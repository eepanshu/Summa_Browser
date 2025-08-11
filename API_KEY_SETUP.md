# 🔑 API Key Configuration Guide

## AssemblyAI API Key Setup

Your AssemblyAI API Key: `3f07e0254b9240a1bef7287cb6a22cdc`

### 🚀 Render Deployment Setup (REQUIRED)

1. **Login to Render**:
   - Go to: https://dashboard.render.com
   - Find your `summabrowser-api` service

2. **Add Environment Variable**:
   - Click on your service
   - Go to **"Environment"** tab
   - Click **"Add Environment Variable"**
   - Enter:
     - **Key**: `ASSEMBLYAI_API_KEY`  
     - **Value**: `3f07e0254b9240a1bef7287cb6a22cdc`

3. **Save and Deploy**:
   - Click **"Save Changes"**
   - Render will automatically redeploy (takes 2-3 minutes)

### 🧪 Test After Setup

Run this command to verify it's working:

```bash
python test_assemblyai_setup.py
```

### ✅ What Will Work After Setup

- ✅ **All YouTube videos** (with or without transcripts)
- ✅ **Video URLs from other platforms**
- ✅ **Full video processing pipeline**
- ✅ **Professional AI summarization**

### 📊 AssemblyAI Usage Limits

- **Free Tier**: 5 hours of audio/video per month
- **Quality**: Professional-grade transcription
- **Speed**: 2-3 minutes processing time per video
- **Features**: Auto-highlights, summaries, key points

### 🔒 Security Notes

- ✅ API key is safely stored in Render environment
- ✅ Not visible in code or git repository
- ✅ Only accessible by your deployed application

### 🚨 If You See Errors

Common error messages and solutions:

| Error Message | Solution |
|---------------|----------|
| "AssemblyAI API key not provided" | Add the environment variable to Render |
| "quota exceeded" or "usage limit" | You've used 5 hours this month |
| "invalid API key" | Double-check the key value |

### 📞 Support

If you need help:
- Check Render dashboard for deployment logs
- Run the test script to verify setup
- AssemblyAI documentation: https://www.assemblyai.com/docs/

---
*Last updated: August 11, 2025*
