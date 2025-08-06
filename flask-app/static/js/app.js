class NewsPortal {
    constructor() {
        this.newsGrid = document.getElementById('newsGrid');
        this.searchInput = document.getElementById('searchInput');
        this.searchBtn = document.getElementById('searchBtn');
        this.loading = document.getElementById('loading');
        this.sectionHeader = document.getElementById('sectionHeader');
        this.sectionTitle = document.getElementById('sectionTitle');
        this.sectionSubtitle = document.getElementById('sectionSubtitle');
        this.categoryList = document.getElementById('categoryList');
        
        this.currentCategory = 'general';
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadDefaultNews();
    }

    bindEvents() {
        this.searchBtn.addEventListener('click', () => this.handleSearch());
        this.searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.handleSearch();
        });

        this.categoryList.addEventListener('click', (e) => {
            if (e.target.classList.contains('category-pill')) {
                this.handleCategoryClick(e.target);
            }
        });
    }

    async handleSearch() {
        const query = this.searchInput.value.trim();
        if (!query) {
            this.showError('Please enter a search term');
            return;
        }
        
        if (query.length < 2) {
            this.showError('Search query must be at least 2 characters');
            return;
        }
        
        await this.fetchSearchResults(query);
    }

    handleCategoryClick(pill) {
        document.querySelectorAll('.category-pill').forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        
        const category = pill.dataset.category;
        this.currentCategory = category;
        this.fetchNewsByCategory(category);
    }

    async loadDefaultNews() {
        await this.fetchNewsByCategory('technology');
    }

    async fetchNewsByCategory(category) {
        this.showLoading();
        
        try {
            const response = await fetch(`/api/news/category/${category}`);
            const data = await response.json();

            if (data.success && data.articles && data.articles.length > 0) {
                this.displayNews(data.articles);
                this.updateSectionHeader(category, 'category');
            } else {
                this.showEmptyState(category);
            }
        } catch (error) {
            console.error('Error fetching news:', error);
            this.showError('Failed to load news. Please check your connection and try again.');
        }
    }

    async fetchSearchResults(query) {
        this.showLoading();
        
        try {
            const response = await fetch(`/api/news/search?q=${encodeURIComponent(query)}&sortBy=publishedAt`);
            const data = await response.json();

            if (data.success && data.articles && data.articles.length > 0) {
                this.displayNews(data.articles);
                this.updateSectionHeader(query, 'search');
            } else {
                this.showEmptyState(query);
            }
        } catch (error) {
            console.error('Error searching news:', error);
            this.showError('Failed to search news. Please try again.');
        }
    }

    displayNews(articles) {
        this.hideLoading();
        this.newsGrid.innerHTML = '';

        articles.slice(0, 12).forEach((article, index) => {
            const newsCard = this.createNewsCard(article);
            newsCard.style.animationDelay = `${index * 0.1}s`;
            this.newsGrid.appendChild(newsCard);
        });
    }

    createNewsCard(article) {
        const card = document.createElement('div');
        card.className = 'news-card fade-in-up';
        
        card.innerHTML = `
            <img src="${article.urlToImage}" alt="News Image" class="card-image" 
                 onerror="this.style.display='none'; this.nextElementSibling.style.paddingTop='1.5rem';">
            <div class="card-content">
                <h3 class="card-title">${this.escapeHtml(article.title)}</h3>
                <p class="card-description">${this.escapeHtml(article.description || 'No description available.')}</p>
                <a href="${article.url}" target="_blank" rel="noopener noreferrer" class="read-more">
                    Read Full Article
                    <i class="fas fa-arrow-right"></i>
                </a>
                <div class="card-meta">
                    <span class="card-source">${this.escapeHtml(article.source.name)}</span>
                    <span class="card-date">
                        <i class="far fa-calendar"></i>
                        ${article.formatted_date || 'Unknown date'}
                    </span>
                </div>
            </div>
        `;

        return card;
    }

    updateSectionHeader(query, type) {
        this.sectionHeader.style.display = 'block';
        
        if (type === 'category') {
            this.sectionTitle.textContent = `${query.charAt(0).toUpperCase() + query.slice(1)} News`;
            this.sectionSubtitle.textContent = `Latest ${query} news and updates`;
        } else {
            this.sectionTitle.textContent = 'Search Results';
            this.sectionSubtitle.textContent = `Results for "${query}"`;
        }
    }

    showLoading() {
        this.loading.style.display = 'block';
        this.newsGrid.innerHTML = '';
        this.sectionHeader.style.display = 'none';
    }

    hideLoading() {
        this.loading.style.display = 'none';
        this.sectionHeader.style.display = 'block';
    }

    showError(message) {
        this.hideLoading();
        this.newsGrid.innerHTML = `
            <div class="error-state fade-in-up">
                <div class="error-icon">
                    <i class="fas fa-exclamation-triangle"></i>
                </div>
                <h3 class="error-title">Something went wrong</h3>
                <p class="error-message">${this.escapeHtml(message)}</p>
            </div>
        `;
    }

    showEmptyState(query) {
        this.hideLoading();
        this.newsGrid.innerHTML = `
            <div class="empty-state fade-in-up">
                <div class="empty-icon">
                    <i class="far fa-newspaper"></i>
                </div>
                <h3 class="empty-title">No Results Found</h3>
                <p class="empty-message">No news articles found for "${this.escapeHtml(query)}". Try different keywords or browse by category.</p>
            </div>
        `;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the news portal when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new NewsPortal();
});


