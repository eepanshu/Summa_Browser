# SummaBrowser Deployment Guide

## 🚀 Live Demo
- **Backend API**: https://summabrowser-api.onrender.com
- **Extension**: Download from GitHub releases

## 📦 Deployment Steps

### Step 1: Deploy Backend to Render

1. **Fork this repository** to your GitHub account

2. **Go to [Render.com](https://render.com)** and create a free account

3. **Create a new Web Service**:
   - Connect your GitHub account
   - Select the forked `Summa_Browser` repository
   - Configure the service:
     - **Name**: `summabrowser-api`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r summary/requirements.txt`
     - **Start Command**: `cd summary && python app.py`
     - **Plan**: Free

4. **Add Environment Variables**:
   ```
   FLASK_ENV=production
   PORT=10000
   ```

5. **Deploy**: Click "Create Web Service"

### Step 2: Update Extension Configuration

1. **Copy your Render URL** (e.g., `https://your-service.onrender.com`)

2. **Update manifest.json**:
   ```json
   {
     "host_permissions": [
       "https://your-service.onrender.com/*"
     ]
   }
   ```

3. **Update popup.js**:
   ```javascript
   this.API_BASE_URL = 'https://your-service.onrender.com';
   ```

### Step 3: Load Extension

1. Open Chrome → `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the SummaBrowse folder
5. Extension ready to use! 🎉

## 🔧 Alternative Deployment Options

### Heroku (Free Tier Discontinued)
- Use the provided `Dockerfile`
- Deploy using Heroku CLI

### Railway
1. Connect GitHub repository
2. Deploy with Python environment
3. Add environment variables

### Vercel (Serverless)
- Use Vercel's Python runtime
- May have limitations with file uploads

### PythonAnywhere
- Upload files manually
- Configure Flask application
- Free tier available

## 📋 Production Checklist

- [ ] Backend deployed and accessible
- [ ] Extension manifest updated with production URL
- [ ] CORS headers configured
- [ ] File size limits set appropriately
- [ ] Error logging configured
- [ ] SSL/HTTPS enabled
- [ ] Extension tested with production API

## 🌐 Making Extension Public

### Chrome Web Store
1. **Package Extension**: Create a ZIP file with all extension files
2. **Developer Account**: Register at [Chrome Web Store Developer Dashboard](https://chrome.google.com/webstore/devconsole/)
3. **Upload**: Submit extension for review
4. **Review**: Usually takes 1-3 days

### Manual Distribution
- Host extension files on GitHub releases
- Users can download and install manually
- Provide installation instructions

## 🔍 Monitoring & Maintenance

### Backend Monitoring
- Check Render dashboard for uptime
- Monitor API response times
- Review error logs

### Extension Updates
- Update version in manifest.json
- Test with different file types
- Monitor user feedback

## 🆘 Troubleshooting

### Common Issues:
1. **CORS Errors**: Ensure backend has proper CORS configuration
2. **File Upload Fails**: Check file size limits and formats
3. **Extension Not Loading**: Verify manifest.json syntax
4. **API Timeout**: Render free tier may have cold starts

### Debug Mode:
Enable in popup.js:
```javascript
console.log('Debug info:', response);
```
