# Sanic + Next.js Template for Vercel

A full-stack template application showcasing **Next.js 14 with TypeScript** frontend and **Sanic Python** backend, designed for seamless deployment on **Vercel's serverless platform**.

## 🎯 Features

### Frontend (Next.js)
- ✅ Next.js 14 with App Router
- ✅ TypeScript for type safety
- ✅ Tailwind CSS for modern styling
- ✅ Responsive design with beautiful UI
- ✅ Real-time API integration
- ✅ Error handling and loading states

### Backend (Sanic)
- ✅ Sanic ASGI framework
- ✅ Modular architecture with blueprints
- ✅ Pydantic for request/response validation
- ✅ Thread-safe mock database
- ✅ CORS middleware
- ✅ Request/response logging
- ✅ Error handling

### Deployment
- ✅ Vercel-ready configuration
- ✅ Serverless function compatibility
- ✅ Development and production environments
- ✅ Environment variable support

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ 
- **Python 3.12** (required for Vercel compatibility)
- npm or yarn

⚠️ **Important**: This template specifically requires Python 3.12 for optimal Vercel serverless function compatibility. Python 3.13 is not yet fully supported by all dependencies.

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd sanic-template-api

# Run the setup script
./dev-setup.sh
```

### 2. Development

Start both frontend and backend:

```bash
# Terminal 1: Start Next.js frontend
npm run dev

# Terminal 2: Start Sanic backend
npm run python-dev
```

Visit:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000

### 3. Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

## 📁 Project Structure

```
sanic-template-api/
├── app/                    # Next.js app directory
│   ├── components/         # React components
│   ├── globals.css         # Global styles
│   ├── layout.tsx          # Root layout
│   └── page.tsx            # Home page
├── api/                    # Python backend
│   ├── modules/            # Modular backend code
│   │   ├── database.py     # Mock database
│   │   ├── middleware.py   # Middleware setup
│   │   ├── users.py        # User endpoints
│   │   └── todos.py        # Todo endpoints
│   ├── requirements.txt    # Python dependencies
│   ├── main.py            # Main app entry point
│   └── index.py           # Vercel handler
├── vercel.json            # Vercel configuration
├── next.config.js         # Next.js configuration
├── package.json           # Node.js dependencies
└── dev-setup.sh          # Development setup script
```

## 🔌 API Endpoints

### Users
- `GET /api/users` - Get all users
- `GET /api/users/{id}` - Get user by ID
- `POST /api/users` - Create new user
- `PUT /api/users/{id}` - Update user
- `DELETE /api/users/{id}` - Delete user

### Todos
- `GET /api/todos` - Get all todos
- `GET /api/todos/{id}` - Get todo by ID
- `POST /api/todos` - Create new todo
- `PUT /api/todos/{id}` - Update todo
- `DELETE /api/todos/{id}` - Delete todo
- `GET /api/users/{id}/todos` - Get user's todos

### Health
- `GET /api/health` - Health check
- `GET /api` - API information

## 💾 Database

The template uses an in-memory mock database for demonstration. In production, you can easily replace it with:

- PostgreSQL (recommended for Vercel)
- MongoDB
- Supabase
- PlanetScale

### Replacing the Mock Database

1. Install your database client (e.g., `psycopg2` for PostgreSQL)
2. Update `api/modules/database.py`
3. Add connection string to environment variables
4. Update the database methods

## 🌐 Environment Variables

### Development (.env.local)
```env
NODE_ENV=development
API_URL=http://localhost:8000
```

### Production (Vercel Dashboard)
```env
NODE_ENV=production
# Add your database URL, API keys, etc.
```

## 🔧 Configuration

### Next.js Configuration
The `next.config.js` handles API proxying:
- Development: Routes `/api/python/*` to `http://localhost:8000/api/*`
- Production: Routes handled by Vercel functions

### Vercel Configuration
The `vercel.json` configures:
- Next.js build for frontend
- Python runtime for backend
- URL routing between frontend and API

## 🧪 Testing

### Frontend Testing
```bash
npm run lint          # ESLint
npm run type-check     # TypeScript checking
```

### Backend Testing
```bash
cd api
source venv/bin/activate
python -m pytest      # Add tests in tests/ directory
```

## 📱 Features Demonstrated

### Frontend Capabilities
- Server-side rendering with App Router
- Client-side state management
- Form handling and validation
- API integration with error handling
- Responsive design
- Loading states and user feedback

### Backend Capabilities
- RESTful API design
- Request validation with Pydantic
- Modular architecture
- Middleware implementation
- Error handling
- CORS configuration
- Thread-safe operations

### Full-Stack Integration
- API communication between frontend and backend
- State synchronization
- Real-time updates
- Error propagation and handling

## 🚀 Production Deployment

### Vercel Deployment

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Connect to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Vercel will automatically detect the configuration

3. **Environment Variables**
   - Add production environment variables in Vercel dashboard
   - Update API URLs and database connections

4. **Deploy**
   - Automatic deployment on every push
   - Preview deployments for pull requests

### Manual Deployment
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

## 🔍 Key Implementation Details

### Serverless Compatibility
- **Stateless Design**: The mock database is thread-safe but stateless across function calls
- **Cold Start Optimization**: Lightweight imports and minimal startup time
- **Function Isolation**: Each API endpoint can run independently

### Modular Architecture
- **Blueprints**: Organized endpoints into logical modules
- **Separation of Concerns**: Database, middleware, and business logic separated
- **Easy Extension**: Add new modules by creating blueprints and registering them

### Development Experience
- **Hot Reload**: Both frontend and backend support hot reloading
- **Type Safety**: Full TypeScript support with proper type definitions
- **Error Handling**: Comprehensive error handling with user-friendly messages

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - feel free to use this template for your projects!

## 🆘 Troubleshooting

### Common Issues

**CORS Errors**
- Ensure `sanic-cors` is installed
- Check CORS middleware configuration
- Verify frontend URL in CORS origins

**API Not Found (404)**
- Check `vercel.json` routing configuration
- Verify API file structure matches Vercel requirements
- Ensure `api/index.py` exists

**Database Connection Issues**
- The mock database is in-memory and resets on function restart
- For persistent data, replace with a real database
- Check database connection strings and credentials

**Build Errors**
- Ensure all dependencies are listed in `package.json` and `requirements.txt`
- Check TypeScript types and fix any type errors
- Verify Python import paths are correct

### Getting Help

- Check the [GitHub Issues](link-to-issues)
- Review [Vercel Documentation](https://vercel.com/docs)
- Check [Sanic Documentation](https://sanic.dev/)
- Review [Next.js Documentation](https://nextjs.org/docs)
