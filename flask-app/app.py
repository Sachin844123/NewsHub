# app.py
from flask import Flask, render_template, request, jsonify
import requests
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
class Config:
    NEWS_API_KEY = os.environ.get('NEWS_API_KEY', 'ee64a70a680d4093906a1cb02bf2dfca')
    NEWS_API_BASE_URL = 'https://newsapi.org/v2'
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')

app.config.from_object(Config)

class NewsService:
    """Service class to handle news API operations"""
    
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({'X-API-Key': self.api_key})
    
    def get_headlines_by_category(self, category='general', country='us', page_size=20):
        """Fetch top headlines by category"""
        try:
            url = f"{self.base_url}/top-headlines"
            params = {
                'category': category,
                'country': country,
                'pageSize': page_size,
                'apiKey': self.api_key
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return self._process_articles(data.get('articles', []))
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching headlines: {e}")
            return {'success': False, 'error': 'Failed to fetch news from API'}
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {'success': False, 'error': 'An unexpected error occurred'}
    
    def search_news(self, query, sort_by='publishedAt', page_size=20):
        """Search for news articles"""
        try:
            url = f"{self.base_url}/everything"
            params = {
                'q': query,
                'sortBy': sort_by,
                'pageSize': page_size,
                'language': 'en',
                'apiKey': self.api_key
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return self._process_articles(data.get('articles', []))
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching news: {e}")
            return {'success': False, 'error': 'Failed to search news'}
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {'success': False, 'error': 'An unexpected error occurred'}
    
    def _process_articles(self, articles):
        """Process and filter articles"""
        if not articles:
            return {'success': True, 'articles': [], 'total': 0}
        
        # Filter articles with required fields
        filtered_articles = []
        for article in articles:
            if all([
                article.get('title'),
                article.get('description'),
                article.get('url'),
                article.get('urlToImage'),
                article.get('publishedAt')
            ]):
                # Format the published date
                try:
                    pub_date = datetime.fromisoformat(article['publishedAt'].replace('Z', '+00:00'))
                    article['formatted_date'] = pub_date.strftime('%b %d, %Y')
                    article['time_ago'] = self._get_time_ago(pub_date)
                except:
                    article['formatted_date'] = 'Unknown'
                    article['time_ago'] = 'Unknown'
                
                # Clean up description
                if article['description']:
                    article['description'] = article['description'][:200] + '...' if len(article['description']) > 200 else article['description']
                
                filtered_articles.append(article)
        
        return {
            'success': True,
            'articles': filtered_articles,
            'total': len(filtered_articles)
        }
    
    def _get_time_ago(self, pub_date):
        """Calculate time ago from published date"""
        now = datetime.now(pub_date.tzinfo)
        diff = now - pub_date
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"

# Initialize news service
news_service = NewsService(app.config['NEWS_API_KEY'], Config.NEWS_API_BASE_URL)

@app.route('/')
def index():
    """Main page route"""
    return render_template('index.html')

@app.route('/api/news/category/<category>')
def get_news_by_category(category):
    """API endpoint to get news by category"""
    try:
        valid_categories = ['general', 'business', 'technology', 'health', 'science', 'sports', 'entertainment']
        
        if category not in valid_categories:
            return jsonify({'success': False, 'error': 'Invalid category'}), 400
        
        result = news_service.get_headlines_by_category(category)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"Error in category endpoint: {e}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

@app.route('/api/news/search')
def search_news():
    """API endpoint to search news"""
    try:
        query = request.args.get('q', '').strip()
        
        if not query:
            return jsonify({'success': False, 'error': 'Search query is required'}), 400
        
        if len(query) < 2:
            return jsonify({'success': False, 'error': 'Search query must be at least 2 characters'}), 400
        
        sort_by = request.args.get('sortBy', 'publishedAt')
        valid_sorts = ['publishedAt', 'relevancy', 'popularity']
        
        if sort_by not in valid_sorts:
            sort_by = 'publishedAt'
        
        result = news_service.search_news(query, sort_by)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"Error in search endpoint: {e}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'NewsHub Pro API'
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    # For development only
    app.run(debug=True, host='0.0.0.0', port=5000)






