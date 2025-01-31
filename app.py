from flask import Flask, request, jsonify, send_file
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask_cors import CORS
import os
from werkzeug.security import generate_password_hash
from apscheduler.schedulers.background import BackgroundScheduler
from flask_mail import Mail, Message
from jinja2 import Template
from celery import Celery
import csv
import time
from io import StringIO
from flask_caching import Cache


app = Flask(__name__)
CORS(app)
api = Api(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///influencer_sponsor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Mail config

# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587   
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'your_email@gmail.com'  # Replace with your email
# app.config['MAIL_PASSWORD'] = 'your_password'  # Replace with your email password

app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 1025
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = "srahulsingh7488@gmail.com"
app.config['MAIL_PASSWORD'] = None

# python -m smtpd -n -c DebuggingServer localhost:1025
# python -m aiosmtpd -n -l localhost:1025

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

cache = Cache(app, config={
    'CACHE_TYPE': 'simple'  # or 'redis' for production
})


db = SQLAlchemy(app)
jwt = JWTManager(app)
mail = Mail(app)


# Ensure upload folder exists
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
# In Flask app
UPLOAD_FOLDER = 'uploads'
os.makedirs(os.path.join(UPLOAD_FOLDER, 'profile_pics'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'campaign_pics'), exist_ok=True)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    # is_flagged = db.Column(db.Boolean, default=False)
    profile_pic = db.Column(db.String(200))

class Sponsor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_name = db.Column(db.String(120))
    industry = db.Column(db.String(120))
    budget = db.Column(db.Float)
    description = db.Column(db.Text)
    is_approved = db.Column(db.Boolean, default=False)

class Influencer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(120))
    category = db.Column(db.String(120))
    niche = db.Column(db.String(120))
    reach = db.Column(db.Integer)
    bio = db.Column(db.Text)

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    budget = db.Column(db.Float)
    category = db.Column(db.String(120))
    status = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    campaign_pic = db.Column(db.String(200))

class AdRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Helper functions
def save_picture(file, folder):
    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], folder, filename)
    file.save(file_path)
    return os.path.join(folder, filename)

# hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

# API Resources
class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        email = data['email']
        password = data['password']
        role = data['role']

        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            return {'message': 'User already exists'}, 400

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.flush()

        if role == 'sponsor':
            new_sponsor = Sponsor(user_id=new_user.id)
            db.session.add(new_sponsor)
        elif role == 'influencer':
            new_influencer = Influencer(user_id=new_user.id)
            db.session.add(new_influencer)

        db.session.commit()

        return {'message': 'User created successfully'}, 201

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        print(f"Login request data: {data}")  # Check if the data is coming through correctly
        user = User.query.filter_by(username=data['username']).first()
        
        if user:
            print(f"Found user: {user.username}")
            if check_password_hash(user.password, data['password']):
                print("Password is correct!")
                if user.role == 'Sponsor' and not Sponsor.query.filter_by(user_id=user.id).first().is_approved:
                    return {'message': 'Sponsor account not yet approved'}, 403
                
                access_token = create_access_token(identity=user.id)
                return {
                    'message': 'Login successful',  
                    'access_token': access_token,
                    'username': user.username,
                    'role': user.role
                }, 200
            else:
                print("Password mismatch!")
        else:
            print("User not found!")

        return {'message': 'Invalid credentials'}, 401



class UserProfile(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role == 'sponsor':
            profile = Sponsor.query.filter_by(user_id=user_id).first()
            return {
                'id': profile.id,
                'company_name': profile.company_name,
                'industry': profile.industry,
                'budget': profile.budget,
                'description': profile.description,
                'profile_pic': user.profile_pic
            }
        elif user.role == 'influencer':
            profile = Influencer.query.filter_by(user_id=user_id).first()
            return {
                'id': profile.id,
                'name': profile.name,
                'category': profile.category,
                'niche': profile.niche,
                'reach': profile.reach,
                'bio': profile.bio,
                'profile_pic': user.profile_pic
            }
    
    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        data = request.get_json()  # Make sure you're using get_json() instead of form

        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            pic_path = save_picture(file, 'profile_pics')
            user.profile_pic = pic_path

        if user.role == 'sponsor':
            profile = Sponsor.query.filter_by(user_id=user_id).first()
            profile.company_name = data.get('company_name', profile.company_name)
            profile.industry = data.get('industry', profile.industry)
            profile.budget = data.get('budget', profile.budget)
            profile.description = data.get('description', profile.description)
        elif user.role == 'influencer':
            profile = Influencer.query.filter_by(user_id=user_id).first()
            profile.name = data.get('name', profile.name)
            profile.category = data.get('category', profile.category)
            profile.niche = data.get('niche', profile.niche)
            profile.reach = data.get('reach', profile.reach)
            profile.bio = data.get('bio', profile.bio)

        db.session.commit()
        return {'message': 'Profile updated successfully'}, 200
    
class CampaignListResource(Resource):
    @jwt_required()
    @cache.memoize(timeout=300)
    def get(self):  # Remove user_id parameter from here
        user_id = get_jwt_identity()  # We already get user_id from JWT
        print("Fetching campaigns...")  # Debug print
        start_time = time.time()
        
        user = User.query.get(user_id)
        if user.role != 'sponsor':
            return {'message': 'Only sponsors can view campaigns'}, 403

        sponsor = Sponsor.query.filter_by(user_id=user_id).first()
        campaigns = Campaign.query.filter_by(sponsor_id=sponsor.id).all()
        
        end_time = time.time()
        print(f"Time taken: {end_time - start_time} seconds")

        return [{
            'id': c.id,
            'title': c.title,
            'description': c.description,
            'budget': c.budget,
            'category': c.category,
            'start_date': c.start_date.isoformat(),
            'end_date': c.end_date.isoformat(),
            'campaign_pic': c.campaign_pic,
            'status': c.status,
            'sponsor_id': c.sponsor_id
        } for c in campaigns]

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'sponsor':
            return {'message': 'Only sponsors can create campaigns'}, 403

        sponsor = Sponsor.query.filter_by(user_id=user_id).first()
        data = request.get_json()
        new_campaign = Campaign(
            sponsor_id=sponsor.id,
            title=data['title'],
            description=data['description'],
            budget=data['budget'],
            category=data['category'],
            status='active',
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d'),
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d')
        )

        if 'campaign_pic' in request.files:
            file = request.files['campaign_pic']
            pic_path = save_picture(file, 'campaign_pics')
            new_campaign.campaign_pic = pic_path

        db.session.add(new_campaign)
        db.session.commit()

        # Invalidate the cache for this user's campaigns
        cache.delete_memoized(self.get, user_id)
        
        return {'message': 'Campaign created successfully'}, 201
        
class AdRequestResource(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'influencer':
            return {'message': 'Only influencers can create ad requests'}, 403

        data = request.get_json()
        influencer = Influencer.query.filter_by(user_id=user_id).first()
        new_ad_request = AdRequest(
            campaign_id=data['campaign_id'],
            influencer_id=influencer.id,
            status='pending',
            details=data.get('details', '')
        )
        db.session.add(new_ad_request)
        db.session.commit()
        return {'message': 'Ad request created successfully'}, 201

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role == 'sponsor':
            sponsor = Sponsor.query.filter_by(user_id=user_id).first()
            ad_requests = AdRequest.query.join(Campaign).filter(Campaign.sponsor_id == sponsor.id).all()
        elif user.role == 'influencer':
            influencer = Influencer.query.filter_by(user_id=user_id).first()
            ad_requests = AdRequest.query.filter_by(influencer_id=influencer.id).all()
        else:
            return {'message': 'Invalid user role'}, 400

        return [
            {
                'id': ar.id,
                'campaign_id': ar.campaign_id,
                'influencer_id': ar.influencer_id,
                'status': ar.status,
                'details': ar.details,
                'created_at': ar.created_at.isoformat(),
                'updated_at': ar.updated_at.isoformat()
            } for ar in ad_requests
        ]

class AdminSponsorApproval(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if user.role != 'admin':
            return {'message': 'Access denied'}, 403

        unapproved_sponsors = Sponsor.query.filter_by(is_approved=False).all()
        
        # Return detailed information on unapproved sponsors
        return {
            'unapproved_sponsors': [
                {
                    'id': s.id,
                    'company_name': s.company_name,
                    'industry': s.industry,
                    'description': s.description,
                } for s in unapproved_sponsors
            ]
        }, 200

    @jwt_required()
    def post(self, sponsor_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if user.role != 'admin':
            return {'message': 'Access denied'}, 403

        sponsor = Sponsor.query.get(sponsor_id)

        if not sponsor:
            return {'message': 'Sponsor not found'}, 404

        sponsor.is_approved = True
        db.session.commit()
        return {'message': 'Sponsor approved successfully'}, 200


# Edit and delete campaigns

class CampaignResource(Resource):
    @jwt_required()
    def get(self, campaign_id=None):
        if campaign_id:
            try:
                campaign = Campaign.query.get(campaign_id)
                if not campaign:
                    return {'message': 'Campaign not found'}, 404

                # Get sponsor information
                sponsor = Sponsor.query.get(campaign.sponsor_id)
                sponsor_user = User.query.get(sponsor.user_id)

                return {
                    'id': campaign.id,
                    'title': campaign.title,
                    'description': campaign.description,
                    'budget': campaign.budget,
                    'category': campaign.category,
                    'status': campaign.status,
                    'start_date': campaign.start_date.isoformat(),
                    'end_date': campaign.end_date.isoformat(),
                    'campaign_pic': campaign.campaign_pic,
                    'sponsor': {
                        'company_name': sponsor.company_name,
                        'email': sponsor_user.email,
                        'industry': sponsor.industry
                    }
                }
            except Exception as e:
                print(f"Error fetching campaign: {str(e)}")
                return {'message': 'Error fetching campaign details'}, 500

    @jwt_required()
    def put(self, campaign_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'sponsor':
            return {'message': 'Only sponsors can edit campaigns'}, 403

        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return {'message': 'Campaign not found'}, 404

        sponsor = Sponsor.query.filter_by(user_id=user_id).first()
        if campaign.sponsor_id != sponsor.id:
            return {'message': 'You can only edit your own campaigns'}, 403

        data = request.get_json()
        campaign.title = data.get('title', campaign.title)
        campaign.description = data.get('description', campaign.description)
        campaign.budget = data.get('budget', campaign.budget)
        campaign.category = data.get('category', campaign.category)
        campaign.status = data.get('status', campaign.status)
        
        if 'start_date' in data:
            campaign.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        if 'end_date' in data:
            campaign.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')

        db.session.commit()
        return {'message': 'Campaign updated successfully'}, 200

    @jwt_required()
    def delete(self, campaign_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'sponsor':
            return {'message': 'Only sponsors can delete campaigns'}, 403

        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return {'message': 'Campaign not found'}, 404

        sponsor = Sponsor.query.filter_by(user_id=user_id).first()
        if campaign.sponsor_id != sponsor.id:
            return {'message': 'You can only delete your own campaigns'}, 403

        db.session.delete(campaign)
        db.session.commit()
        return {'message': 'Campaign deleted successfully'}, 200

# Search Influencers

class InfluencerSearch(Resource):
    @jwt_required()
    @cache.memoize(timeout=300)  # Cache for 5 minutes
    def get(self):
        print("Searching influencers...")  # Debug print
        start_time = time.time()

        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'sponsor':
            return {'message': 'Only sponsors can search for influencers'}, 403

        category = request.args.get('category')
        niche = request.args.get('niche')
        min_reach = request.args.get('min_reach', type=int)

        # Start with base query
        query = Influencer.query

        # Only get influencers with complete profiles
        query = query.filter(
            Influencer.name.isnot(None),
            Influencer.category.isnot(None),
            Influencer.niche.isnot(None),
            Influencer.reach.isnot(None)
        )

        # Apply filters
        if category:
            query = query.filter(Influencer.category.ilike(f'%{category}%'))
        if niche:
            query = query.filter(Influencer.niche.ilike(f'%{niche}%'))
        if min_reach:
            query = query.filter(Influencer.reach >= min_reach)

        influencers = query.all()

        print(f"Search time: {time.time() - start_time} seconds")  # Debug print

        return [{
            'id': inf.id,
            'name': inf.name,
            'category': inf.category,
            'niche': inf.niche,
            'reach': inf.reach,
            'bio': inf.bio or ''  # Return empty string if bio is None
        } for inf in influencers], 200

    # Method to invalidate cache when an influencer updates their profile
    def invalidate_search_cache(self):
        cache.delete_memoized(self.get)

# search campaigns

class CampaignSearch(Resource):
   @jwt_required()
   @cache.memoize(timeout=300)  # Cache for 5 minutes
   def get(self):
       print("Searching campaigns...")  # Debug print
       start_time = time.time()

       user_id = get_jwt_identity()
       user = User.query.get(user_id)
       if user.role != 'influencer':
           return {'message': 'Only influencers can search for campaigns'}, 403

       category = request.args.get('category')
       min_budget = request.args.get('min_budget', type=float)
       start_date = request.args.get('start_date') 
       end_date = request.args.get('end_date')

       query = Campaign.query.filter_by(status='active')

       if category:
           query = query.filter(Campaign.category == category)
       if min_budget:
           query = query.filter(Campaign.budget >= min_budget)
       if start_date:
           query = query.filter(Campaign.start_date >= datetime.strptime(start_date, '%Y-%m-%d'))
       if end_date:
           query = query.filter(Campaign.end_date <= datetime.strptime(end_date, '%Y-%m-%d'))

       campaigns = query.all()

       print(f"Search time: {time.time() - start_time} seconds")  # Debug print

       return [{
           'id': c.id,
           'title': c.title,
           'description': c.description,
           'budget': c.budget,
           'category': c.category,
           'start_date': c.start_date.isoformat(),
           'end_date': c.end_date.isoformat(),
           'campaign_pic': c.campaign_pic
       } for c in campaigns], 200

   # Method to invalidate cache when campaigns are updated/created
   def invalidate_search_cache(self):
       cache.delete_memoized(self.get)

# let's send some adrequests

class SendAdRequest(Resource):
    @jwt_required()
    def post(self, influencer_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'sponsor':
            return {'message': 'Only sponsors can send ad requests'}, 403

        sponsor = Sponsor.query.filter_by(user_id=user_id).first()
        influencer = Influencer.query.get(influencer_id)
        if not influencer:
            return {'message': 'Influencer not found'}, 404

        data = request.get_json()
        campaign_id = data.get('campaign_id')
        campaign = Campaign.query.get(campaign_id)
        if not campaign or campaign.sponsor_id != sponsor.id:
            return {'message': 'Invalid campaign'}, 400

        new_ad_request = AdRequest(
            campaign_id=campaign_id,
            influencer_id=influencer_id,
            status='pending',
            details=data.get('details', '')
        )
        db.session.add(new_ad_request)
        db.session.commit()

        return {'message': 'Ad request sent successfully'}, 201

    @jwt_required()
    def get(self, influencer_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'sponsor':
            return {'message': 'Access denied'}, 403

        sponsor = Sponsor.query.filter_by(user_id=user_id).first()
        ad_requests = AdRequest.query.join(Campaign).filter(
            Campaign.sponsor_id == sponsor.id,
            AdRequest.influencer_id == influencer_id
        ).all()

        return [
            {
                'id': ar.id,
                'campaign_id': ar.campaign_id,
                'status': ar.status,
                'details': ar.details,
                'created_at': ar.created_at.isoformat(),
                'updated_at': ar.updated_at.isoformat()
            } for ar in ad_requests
        ], 200
    
# influencer should view the adrequests also

class InfluencerAdRequests(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'influencer':
            return {'message': 'Access denied'}, 403

        influencer = Influencer.query.filter_by(user_id=user_id).first()
        ad_requests = AdRequest.query.filter_by(influencer_id=influencer.id).all()

        return [
            {
                'id': ar.id,
                'campaign_id': ar.campaign_id,
                'status': ar.status,
                'details': ar.details,
                'created_at': ar.created_at.isoformat(),
                'updated_at': ar.updated_at.isoformat()
            } for ar in ad_requests
        ], 200

    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'influencer':
            return {'message': 'Access denied'}, 403

        data = request.get_json()
        ad_request_id = data.get('ad_request_id')
        action = data.get('action')

        if not ad_request_id or action not in ['accept', 'reject']:
            return {'message': 'Invalid request'}, 400

        influencer = Influencer.query.filter_by(user_id=user_id).first()
        ad_request = AdRequest.query.filter_by(id=ad_request_id, influencer_id=influencer.id).first()

        if not ad_request:
            return {'message': 'Ad request not found'}, 404

        if ad_request.status != 'pending':
            return {'message': 'Can only accept or reject pending ad requests'}, 400

        ad_request.status = 'accepted' if action == 'accept' else 'rejected'
        db.session.commit()

        return {'message': f'Ad request {action}ed successfully'}, 200
    
# let's edit and delete adrequest

class SponsorAdRequest(Resource):
    @jwt_required()
    def get(self, ad_request_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'sponsor':
            return {'message': 'Access denied'}, 403

        sponsor = Sponsor.query.filter_by(user_id=user_id).first()
        ad_request = AdRequest.query.join(Campaign).filter(
            AdRequest.id == ad_request_id,
            Campaign.sponsor_id == sponsor.id
        ).first()

        if not ad_request:
            return {'message': 'Ad request not found'}, 404

        return {
            'id': ad_request.id,
            'campaign_id': ad_request.campaign_id,
            'influencer_id': ad_request.influencer_id,
            'status': ad_request.status,
            'details': ad_request.details,
            'created_at': ad_request.created_at.isoformat(),
            'updated_at': ad_request.updated_at.isoformat()
        }, 200

    @jwt_required()
    def put(self, ad_request_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'sponsor':
            return {'message': 'Access denied'}, 403

        sponsor = Sponsor.query.filter_by(user_id=user_id).first()
        ad_request = AdRequest.query.join(Campaign).filter(
            AdRequest.id == ad_request_id,
            Campaign.sponsor_id == sponsor.id
        ).first()

        if not ad_request:
            return {'message': 'Ad request not found'}, 404

        if ad_request.status != 'pending':
            return {'message': 'Can only edit pending ad requests'}, 400

        data = request.get_json()
        ad_request.details = data.get('details', ad_request.details)
        db.session.commit()

        return {'message': 'Ad request updated successfully'}, 200

    @jwt_required()
    def delete(self, ad_request_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'sponsor':
            return {'message': 'Access denied'}, 403

        sponsor = Sponsor.query.filter_by(user_id=user_id).first()
        ad_request = AdRequest.query.join(Campaign).filter(
            AdRequest.id == ad_request_id,
            Campaign.sponsor_id == sponsor.id
        ).first()

        if not ad_request:
            return {'message': 'Ad request not found'}, 404

        if ad_request.status != 'pending':
            return {'message': 'Can only delete pending ad requests'}, 400

        db.session.delete(ad_request)
        db.session.commit()

        return {'message': 'Ad request deleted successfully'}, 200  

# Admin dashboard resources

from flask import jsonify
from sqlalchemy import func

class AdminDashboard(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'admin':
            return {'message': 'Access denied'}, 403

        # Get statistics
        total_users = User.query.count()
        active_users = User.query.filter_by(is_active=True).count()
        total_sponsors = Sponsor.query.count()
        total_influencers = Influencer.query.count()
        total_campaigns = Campaign.query.count()
        active_campaigns = Campaign.query.filter_by(status='active').count()
        total_ad_requests = AdRequest.query.count()
        pending_ad_requests = AdRequest.query.filter_by(status='pending').count()

        # Get flagged users (commented out for now)
        # flagged_users = User.query.filter_by(is_flagged=True).count()

        # Get recent activities
        recent_campaigns = Campaign.query.order_by(Campaign.id.desc()).limit(5).all()
        recent_ad_requests = AdRequest.query.order_by(AdRequest.id.desc()).limit(5).all()

        return {
            'statistics': {
                'total_users': total_users,
                'active_users': active_users,
                'total_sponsors': total_sponsors,
                'total_influencers': total_influencers,
                'total_campaigns': total_campaigns,
                'active_campaigns': active_campaigns,
                'total_ad_requests': total_ad_requests,
                'pending_ad_requests': pending_ad_requests,
                # 'flagged_users': flagged_users
            },
            'recent_campaigns': [
                {
                    'id': c.id,
                    'title': c.title,
                    'sponsor_id': c.sponsor_id,
                    'status': c.status
                } for c in recent_campaigns
            ],
            'recent_ad_requests': [
                {
                    'id': ar.id,
                    'campaign_id': ar.campaign_id,
                    'influencer_id': ar.influencer_id,
                    'status': ar.status
                } for ar in recent_ad_requests
            ]
        }

# admin managing campaigns and users
class AdminUserManagement(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'admin':
            return {'message': 'Access denied'}, 403

        users = User.query.all()
        return jsonify([
            {
                'id': u.id,
                'username': u.username,
                'email': u.email,
                'role': u.role,
                'is_active': u.is_active,
                # 'is_flagged': u.is_flagged
            } for u in users
        ])

    @jwt_required()
    def put(self, user_id):
        admin_id = get_jwt_identity()
        admin = User.query.get(admin_id)
        if admin.role != 'admin':
            return {'message': 'Access denied'}, 403

        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        data = request.get_json()
        user.is_active = data.get('is_active', user.is_active)
        # user.is_flagged = data.get('is_flagged', user.is_flagged)
        db.session.commit()

        return {'message': 'User updated successfully'}, 200

class AdminCampaignManagement(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'admin':
            return {'message': 'Access denied'}, 403

        campaigns = Campaign.query.all()
        return jsonify([
            {
                'id': c.id,
                'title': c.title,
                'sponsor_id': c.sponsor_id,
                'status': c.status,
                'budget': c.budget,
                'start_date': c.start_date.isoformat(),
                'end_date': c.end_date.isoformat()
            } for c in campaigns
        ])

    @jwt_required()
    def put(self, campaign_id):
        admin_id = get_jwt_identity()
        admin = User.query.get(admin_id)
        if admin.role != 'admin':
            return {'message': 'Access denied'}, 403

        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return {'message': 'Campaign not found'}, 404

        data = request.get_json()
        campaign.status = data.get('status', campaign.status)
        db.session.commit()

        return {'message': 'Campaign updated successfully'}, 200

# generating campaign csv using celery


@celery.task
def generate_campaign_csv(sponsor_id):
    with app.app_context():
        sponsor = Sponsor.query.get(sponsor_id)
        campaigns = Campaign.query.filter_by(sponsor_id=sponsor_id).all()

        csv_file = StringIO()
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Title', 'Description', 'Start Date', 'End Date', 'Budget', 'Status', 'Category'])

        for campaign in campaigns:
            csv_writer.writerow([
                campaign.title,
                campaign.description,
                campaign.start_date,
                campaign.end_date,
                campaign.budget,
                campaign.status,
                campaign.category
            ])

        csv_content = csv_file.getvalue()
        
        # Save CSV to a file
        filename = f"campaign_export_{sponsor_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'w') as f:
            f.write(csv_content)

        # Send email notification
        user = User.query.get(sponsor.user_id)
        msg = Message('Campaign Export Ready',
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[user.email])
        msg.body = f"Your campaign export is ready. You can download it from the dashboard."
        mail.send(msg)

        return filename

class ExportCampaigns(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'sponsor':
            return {'message': 'Access denied'}, 403

        sponsor = Sponsor.query.filter_by(user_id=user_id).first()
        task = generate_campaign_csv.delay(sponsor.id)
        
        return {'message': 'Export job started. You will receive an email when it\'s ready.'}, 202

class DownloadExport(Resource):
    @jwt_required()
    def get(self, filename):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'sponsor':
            return {'message': 'Access denied'}, 403

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(file_path):
            return {'message': 'File not found'}, 404

        return send_file(file_path, as_attachment=True)


# FUNCTIONS OF BACKEND JOBS

# SEND REMINDER MAILS
def send_reminder_emails():
    with app.app_context():
        influencers = Influencer.query.all()
        for influencer in influencers:
            user = User.query.get(influencer.user_id)
            pending_requests = AdRequest.query.filter_by(influencer_id=influencer.id, status='pending').count()
            
            if pending_requests > 0:
                msg = Message('Reminder: Pending Ad Requests',
                              sender=app.config['MAIL_USERNAME'],
                              recipients=[user.email])
                msg.body = f"Hello {influencer.name},\n\nYou have {pending_requests} pending ad request(s). Please log in to review and respond to these requests.\n\nBest regards,\nYour Platform Team"
                mail.send(msg)


# SEND MONTHLY REPORTS
def generate_monthly_report(sponsor):
    # Get all campaigns for this sponsor
    campaigns = Campaign.query.filter_by(sponsor_id=sponsor.id).all()
    
    # Simulate some data (replace with real data in production)
    total_ads = sum(len(AdRequest.query.filter_by(campaign_id=c.id, status='accepted').all()) for c in campaigns)
    total_budget = sum(c.budget for c in campaigns)
    budget_used = round(total_budget * 0.7, 2)  # Simulating 70% budget usage
    budget_remaining = round(total_budget - budget_used, 2)
    sales_growth = round(total_ads * 1000, 2)  # Simulating $1000 growth per ad
    
    # HTML template for the report
    template_string = """
    <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <h1>Monthly Activity Report for {{ sponsor.company_name }}</h1>
            <h2>Summary</h2>
            <p>Total Campaigns: {{ campaigns|length }}</p>
            <p>Total Advertisements: {{ total_ads }}</p>
            <p>Total Budget: ${{ total_budget }}</p>
            <p>Budget Used: ${{ budget_used }}</p>
            <p>Budget Remaining: ${{ budget_remaining }}</p>
            <p>Estimated Sales Growth: ${{ sales_growth }}</p>
            
            <h2>Campaign Details</h2>
            <table>
                <tr>
                    <th>Campaign</th>
                    <th>Start Date</th>
                    <th>End Date</th>
                    <th>Budget</th>
                    <th>Status</th>
                </tr>
                {% for campaign in campaigns %}
                <tr>
                    <td>{{ campaign.title }}</td>
                    <td>{{ campaign.start_date.strftime('%Y-%m-%d') }}</td>
                    <td>{{ campaign.end_date.strftime('%Y-%m-%d') }}</td>
                    <td>${{ campaign.budget }}</td>
                    <td>{{ campaign.status }}</td>
                </tr>
                {% endfor %}
            </table>
        </body>
    </html>
    """
    
    template = Template(template_string)
    return template.render(sponsor=sponsor, campaigns=campaigns, total_ads=total_ads,
                           total_budget=total_budget, budget_used=budget_used,
                           budget_remaining=budget_remaining, sales_growth=sales_growth)

def send_monthly_reports():
    with app.app_context():
        sponsors = Sponsor.query.all()
        for sponsor in sponsors:
            user = User.query.get(sponsor.user_id)
            report_html = generate_monthly_report(sponsor)
            
            msg = Message('Monthly Activity Report',
                          sender=app.config['MAIL_USERNAME'],
                          recipients=[user.email])
            msg.html = report_html
            mail.send(msg)
            print(f"Sent monthly report to {user.email}")

# STARTING SCHEDULER
scheduler = BackgroundScheduler()

# scheduler.add_job(func=send_reminder_emails, trigger="cron", hour=18)  # Sends reminder at 6 PM every day
# scheduler.add_job(func=send_monthly_reports, trigger="cron", day=1, hour=0)  # Sends monthly report on the 1st day of each month at midnight

scheduler.add_job(func=send_reminder_emails, trigger="interval", minutes=1)
scheduler.add_job(func=send_monthly_reports, trigger="interval", minutes=1)


scheduler.start()


# API routes
api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserProfile, '/profile')
api.add_resource(CampaignListResource, '/campaigns')
api.add_resource(AdRequestResource, '/ad_requests')
api.add_resource(AdminSponsorApproval, '/admin/approve_sponsors', '/admin/approve_sponsors/<int:sponsor_id>')
api.add_resource(CampaignResource, '/campaigns', '/campaigns/<int:campaign_id>')
api.add_resource(InfluencerSearch, '/search_influencers')       
api.add_resource(CampaignSearch, '/search_campaigns')
api.add_resource(SendAdRequest, '/send_ad_request/<int:influencer_id>')                                                                         
api.add_resource(InfluencerAdRequests, '/influencer_ad_requests', '/influencer_ad_requests/<int:ad_request_id>')
api.add_resource(SponsorAdRequest, '/sponsor_ad_request/<int:ad_request_id>')  
api.add_resource(AdminDashboard, '/admin/dashboard')
api.add_resource(AdminUserManagement, '/admin/users', '/admin/users/<int:user_id>')
api.add_resource(AdminCampaignManagement, '/admin/campaigns', '/admin/campaigns/<int:campaign_id>')
api.add_resource(ExportCampaigns, '/export_campaigns')
api.add_resource(DownloadExport, '/download_export/<string:filename>')



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)