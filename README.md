# Ocean Adventure with Reefy

An interactive ocean exploration experience with Reefy the friendly shark! Learn about marine life, ocean ecosystems, and conservation through an engaging chat interface powered by AI.

## Features

- Interactive chapters about different ocean environments
- AI-powered chat with Reefy, your ocean guide
- Beautiful ocean-themed UI with animations
- Educational content about marine life

## Setup

1. Clone the repository
```bash
git clone [your-repo-url]
cd ocean-adventure
```

2. Install dependencies for the Netlify functions
```bash
cd netlify/functions
npm install
```

3. Set up environment variables
- Create an OpenAI API key
- Add it to your Netlify environment variables as `OPENAI_API_KEY`

## Deployment

This project is set up for deployment on Netlify:

1. Push your code to GitHub
2. Connect your repository to Netlify
3. Set the following build settings:
   - Build command: `none` (static site)
   - Publish directory: `/`
4. Add your environment variables in Netlify's dashboard
5. Deploy!

## Development

To run locally with Netlify Functions:
```bash
netlify dev
```

## License

MIT
