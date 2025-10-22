# Travel Planner AI 🌍✈️

A modern, full-featured travel planning AI assistant powered by **Google's Gemini 2.5 Flash** model.

## Features

### 🤖 AI Capabilities
- **Expert Travel Planning**: Destination recommendations, itinerary creation, budget optimization
- **Real-time Conversation Context**: Remembers your preferences across the entire conversation
- **Streaming Responses**: See AI responses appear in real-time for better UX
- **Rich Formatting**: Clean, organized responses with sections and recommendations

### 💬 Modern Chatbot Features
- **Multi-turn Conversations**: Seamless context preservation across messages
- **Conversation History**: Keep track of multiple travel planning sessions
- **Clean, Intuitive UI**: Modern web interface with smooth animations
- **Message Suggestions**: Quick-start suggestions for common queries
- **Load/Switch Conversations**: Easily manage multiple trip plans

### 🎯 Travel Planning Capabilities
- **Destination Recommendations**: Based on interests, budget, and season
- **Itinerary Planning**: Day-by-day activity suggestions and timings
- **Budget Optimization**: Cost breakdowns and money-saving tips
- **Flight & Hotel Recommendations**: Smart accommodation suggestions
- **Local Tips**: Restaurant recommendations, local customs, transportation
- **Visa & Documentation**: Travel requirement information
- **Best Time to Visit**: Weather patterns and seasonal advice
- **Off-the-Beaten-Path**: Hidden gems and unique experiences

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Get your free Gemini API key
3. Update the `.env` file:

```
GEMINI_API_KEY=your_api_key_here
```

### 3. Run the Application

```bash
python main.py
```

The application will start at `http://localhost:8000`

## Architecture

### Backend
- **FastAPI**: High-performance Python web framework
- **Gemini 2.5 Flash**: Latest Google generative AI model
- **Streaming Responses**: Real-time response delivery
- **In-Memory Storage**: Conversation history management (upgrade to database for production)

### Frontend
- **HTML5/CSS3**: Modern responsive design
- **Vanilla JavaScript**: No framework dependencies for quick loading
- **Real-time Streaming**: SSE (Server-Sent Events) for live responses
- **Mobile Responsive**: Works seamlessly on all devices

## API Endpoints

### Chat
- **POST** `/api/chat`
  - Send message and stream response
  - Body: `{"content": "message", "conversation_id": "id"}`

### Conversations
- **GET** `/api/conversations/{id}` - Get conversation history
- **POST** `/api/conversations/{id}/clear` - Clear conversation
- **GET** `/api/health` - Health check

## Usage Examples

### Start Planning a Trip
```
"Plan a 2-week trip to Thailand for $2000"
```

### Get Budget Breakdown
```
"Give me a detailed budget breakdown for a week in Paris"
```

### Ask for Recommendations
```
"Best hidden beaches in Indonesia"
```

### Create an Itinerary
```
"Create a 5-day itinerary for London including museums, restaurants, and local experiences"
```

### Travel Tips
```
"What should I know before visiting Japan for the first time?"
```

## Enhancement Ideas

### Immediate Upgrades
- [ ] Integrate with Skyscanner API for real flights
- [ ] Google Hotels API integration
- [ ] Weather API for real-time climate data
- [ ] Visa requirements API
- [ ] Google Maps integration for route planning

### Advanced Features
- [ ] Image upload for destination inspiration
- [ ] Voice input/output support
- [ ] PDF itinerary export
- [ ] Trip sharing and collaboration
- [ ] Expense tracker and splitting
- [ ] User authentication and profiles
- [ ] Database integration for persistent storage
- [ ] Rate limiting and usage analytics

### Frontend Improvements
- [ ] Map visualization for destinations
- [ ] Calendar view for itinerary planning
- [ ] Price comparison charts
- [ ] Photo gallery integration
- [ ] Dark mode support
- [ ] Keyboard shortcuts

## File Structure

```
.
├── main.py              # FastAPI backend
├── static/
│   └── index.html       # Web interface
├── .env                 # API keys (create this)
└── requirements.txt     # Python dependencies
```

## Troubleshooting

### "GEMINI_API_KEY not set" Error
- Make sure `.env` file exists in the project root
- Verify your API key is correctly added
- Restart the application

### CORS Errors
- CORS is enabled for all origins in development
- For production, update `allow_origins` in `main.py`

### API Rate Limits
- Gemini 2.5 Flash has generous free tier limits
- Monitor usage at [Google AI Studio](https://aistudio.google.com/)

## Performance Notes

- **Gemini 2.5 Flash**: Fastest and most efficient model (~15ms latency)
- **Streaming**: Reduces perceived latency - users see responses as they're generated
- **Client-side Processing**: Minimal server load, scalable architecture

## Future Roadmap

1. **Database Integration**: Replace in-memory storage with PostgreSQL
2. **Authentication**: User accounts and authentication system
3. **Real API Integration**: Live flight/hotel search capabilities
4. **Mobile App**: Native iOS and Android apps
5. **Team Features**: Shared trip planning and collaboration
6. **Monetization**: Premium features and subscription model

## Security Notes

- Never commit `.env` file with real API keys
- Implement rate limiting for production
- Add authentication for user data protection
- Validate all user inputs on backend
- Use environment variables for all sensitive data

## License

MIT License - Feel free to use and modify!

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the Gemini API documentation
3. Check browser console for error messages

---

Happy travels! 🌏✈️