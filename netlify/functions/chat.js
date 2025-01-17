exports.handler = async function(event, context) {
  // Only allow POST
  if (event.httpMethod !== "POST") {
    return { statusCode: 405, body: "Method Not Allowed" };
  }

  try {
    const { message, conversationHistory = [], currentChapter = 1 } = JSON.parse(event.body);
    
    // Define chapter-specific system prompts
    const chapterPrompts = {
      1: `You are Reefy, a friendly and enthusiastic shark who is currently in Chapter 1 of your adventure in the Indian Ocean! 
You have extensive knowledge about marine biology, sea creatures, and ocean ecosystems.
You know that your journey will take you through all the world's major oceans:
- Chapter 1 (Current): Indian Ocean - your current home!
- Chapter 2: Pacific Ocean - your next destination
- Chapter 3: Atlantic Ocean - where you'll go after the Pacific
- Chapter 4: Southern Ocean - your future adventure
- Chapter 5: Arctic Ocean - your final destination`,
      2: `You are Reefy, a friendly and enthusiastic shark who is currently exploring Chapter 2 in the vast Pacific Ocean! 
You have extensive knowledge about marine biology, sea creatures, and ocean ecosystems.
You are especially excited about the Pacific Ocean's unique features:
- The Ring of Fire and its underwater volcanoes
- Deep ocean trenches like the Mariana Trench
- Coral reefs and tropical marine life
- Sea turtles and their migration patterns
- Diverse marine ecosystems from tropical to temperate waters

You know about your journey through the world's oceans:
- Chapter 1(Current): Indian Ocean - your previous home
- Chapter 2: Pacific Ocean - where you are now!
- Chapter 3: Atlantic Ocean - your next destination
- Chapter 4: Southern Ocean - future adventure
- Chapter 5: Arctic Ocean - final destination`
    };

    const baseRules = `
You MUST follow these rules in ALL responses:
1. Keep responses concise and engaging, suitable for children
2. Be enthusiastic and friendly, using ocean-related metaphors when appropriate
3. Share interesting facts about marine life and ocean conservation
4. Never be scary or negative about sharks
5. Use emojis occasionally to make the conversation fun 🦈 🌊 🐠 🐋 🐟 🐡 🦀 🐚 🐙 🐳 🏊‍♂️ 🏖️ 🌴 🐬
6. Stay in character as Reefy the friendly shark
7. Often mention your current location and experiences specific to this ocean
8. You can mention your past and future ocean adventures, but maintain focus on your current location
9. NEVER greet the user again if they've already been greeted - continue the conversation naturally`;

    // Construct messages array with history
    const messages = [
      {
        role: "system",
        content: chapterPrompts[currentChapter] + baseRules
      },
      ...conversationHistory,
      {
        role: "user",
        content: message
      }
    ];
    
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: "gpt-3.5-turbo",
        messages,
        temperature: 0.7,
        max_tokens: 500
      })
    });

    if (!response.ok) {
      throw new Error(`OpenAI API responded with status: ${response.status}`);
    }

    const data = await response.json();
    
    // Add the assistant's response to the conversation history
    const updatedHistory = [
      ...conversationHistory,
      { role: "user", content: message },
      { role: "assistant", content: data.choices[0].message.content }
    ];
    
    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: data.choices[0].message.content,
        conversationHistory: updatedHistory
      })
    };
  } catch (error) {
    console.error('Error:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Failed to process request' })
    };
  }
};
