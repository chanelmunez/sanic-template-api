# Deployment Guide

This guide provides detailed instructions for deploying your Sanic + Next.js application to Vercel.

## 📋 Pre-Deployment Checklist

### ✅ Frontend Ready
- [ ] Next.js app builds successfully (`npm run build`)
- [ ] All TypeScript errors resolved
- [ ] Environment variables configured
- [ ] API routing tested locally

### ✅ Backend Ready
- [ ] Sanic app runs without errors
- [ ] All Python dependencies in `requirements.txt`
- [ ] API endpoints tested and working
- [ ] Database connections configured (if using external DB)

### ✅ Configuration Ready
- [ ] `vercel.json` configured correctly
- [ ] Environment variables defined
- [ ] CORS settings updated for production domain
- [ ] API routes match Vercel function structure

## 🚀 Deployment Methods

## ⚠️ Current Status

**Frontend**: ✅ Ready for Vercel deployment (Next.js)
**Backend**: ⚠️ May require configuration adjustments for Vercel serverless functions

The template is fully functional for local development. For production deployment, consider these options:

### Option 1: Frontend-Only on Vercel
Deploy only the Next.js frontend to Vercel and use a different platform for the Python backend:
- **Frontend**: Vercel (recommended)
- **Backend**: Railway, Render, DigitalOcean App Platform, or Heroku

### Option 2: Full-Stack Alternative Platforms
Deploy both frontend and backend to platforms that better support Python:
- **Railway**: Excellent Python support with automatic deployments
- **Render**: Good for full-stack applications
- **DigitalOcean App Platform**: Supports both Next.js and Python

### Method 1: GitHub Integration (Recommended for Frontend)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/username/repository.git
   git push -u origin main
   ```

2. **Connect to Vercel**
   - Visit [vercel.com](https://vercel.com)
   - Click "Import Project"
   - Select your GitHub repository
   - Vercel will auto-detect the framework

3. **Configure Build Settings**
   - Framework Preset: Next.js
   - Root Directory: `./` (leave blank)
   - Build Command: `npm run build`
   - Output Directory: `.next`
   - Install Command: `npm install`

4. **Set Environment Variables**
   ```env
   NODE_ENV=production
   ```

5. **Deploy**
   - Click "Deploy"
   - Automatic deployments on every push

### Method 2: Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Login**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   # First deployment
   vercel

   # Production deployment
   vercel --prod
   ```

## 🔧 Configuration Details

### vercel.json Explanation

```json
{
  "version": 2,
  "builds": [
    {
      "src": "next.config.js",
      "use": "@vercel/next"
    },
    {
      "src": "api/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/python/(.*)",
      "dest": "/api/main.py"
    },
    {
      "src": "/(.*)",
      "dest": "/$1"
    }
  ],
  "functions": {
    "api/main.py": {
      "runtime": "python3.9"
    }
  }
}
```

**Key Points:**
- `builds`: Defines how to build frontend (Next.js) and backend (Python)
- `routes`: URL routing between frontend and serverless functions
- `functions`: Runtime configuration for Python functions

### Environment Variables

#### Development
Create `.env.local`:
```env
NODE_ENV=development
API_URL=http://localhost:8000
```

#### Production
Set in Vercel Dashboard:
```env
NODE_ENV=production
# Add database URLs, API keys, etc.
```

## 🐛 Troubleshooting Deployment

### Common Deployment Issues

#### 1. Build Failures

**Python Import Errors**
```bash
# Error: ModuleNotFoundError
# Solution: Ensure all imports use relative paths
from .database import get_db  # ✅ Correct
from database import get_db   # ❌ May fail in serverless
```

**Missing Dependencies**
```bash
# Error: Package not found
# Solution: Add to requirements.txt
pip freeze > api/requirements.txt
```

#### 2. Runtime Errors

**CORS Issues**
```python
# Update CORS configuration for production domain
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",  # Development
            "https://your-app.vercel.app"  # Production
        ]
    }
})
```

**API Route Not Found**
- Check `vercel.json` routes configuration
- Ensure API files are in correct structure
- Verify function exports

#### 3. Performance Issues

**Cold Start Optimization**
```python
# Minimize imports in main.py
# Use lazy loading for heavy operations
# Keep function memory footprint small
```

**Function Timeout**
```json
{
  "functions": {
    "api/main.py": {
      "runtime": "python3.9",
      "maxDuration": 30
    }
  }
}
```

### Debugging Production Issues

#### 1. Check Vercel Function Logs
```bash
vercel logs
```

#### 2. Test API Endpoints
```bash
# Test production API
curl https://your-app.vercel.app/api/health

# Test specific endpoints
curl -X POST https://your-app.vercel.app/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com"}'
```

#### 3. Monitor Performance
- Use Vercel Analytics
- Check function execution times
- Monitor error rates

## 🔄 Continuous Deployment

### Automatic Deployments

**Branch Configuration**
- `main` branch → Production deployment
- `develop` branch → Preview deployment
- Pull requests → Preview deployments

**Environment-Specific Configs**
```bash
# Different configs per environment
vercel env add NODE_ENV production
vercel env add NODE_ENV preview
```

### Pre-Deploy Hooks

Add to `package.json`:
```json
{
  "scripts": {
    "vercel-build": "npm run build",
    "build": "next build && npm run build:api",
    "build:api": "cd api && pip install -r requirements.txt"
  }
}
```

## 🔒 Security Considerations

### Environment Variables
- Never commit secrets to Git
- Use Vercel environment variables for sensitive data
- Rotate API keys regularly

### CORS Configuration
```python
# Production CORS settings
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://your-domain.com"],  # Specific domain
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

### Rate Limiting
```python
# Add rate limiting for production
# Consider using external services like Upstash Redis
```

## 📊 Monitoring and Analytics

### Vercel Analytics
- Enable in Vercel dashboard
- Monitor page views and performance
- Track Core Web Vitals

### Custom Monitoring
```python
# Add logging for production
import logging

logger = logging.getLogger(__name__)

@app.middleware("request")
async def log_requests(request):
    logger.info(f"Request: {request.method} {request.path}")
```

## 🚀 Performance Optimization

### Frontend Optimization
```javascript
// next.config.js
const nextConfig = {
  experimental: {
    appDir: true,
  },
  compress: true,
  poweredByHeader: false,
  generateEtags: true,
}
```

### Backend Optimization
```python
# Optimize Sanic for serverless
app.config.KEEP_ALIVE_TIMEOUT = 5
app.config.KEEP_ALIVE = False
```

### Database Optimization
- Use connection pooling
- Implement caching strategies
- Optimize queries
- Consider using Vercel's Edge Runtime for simple operations

## 📈 Scaling Considerations

### Horizontal Scaling
- Vercel automatically scales serverless functions
- Consider database connection limits
- Implement proper error handling for high load

### Vertical Scaling
```json
{
  "functions": {
    "api/main.py": {
      "runtime": "python3.9",
      "memory": 512,
      "maxDuration": 30
    }
  }
}
```

### Database Scaling
- Use managed database services (Supabase, PlanetScale)
- Implement read replicas
- Consider caching layers (Redis)
