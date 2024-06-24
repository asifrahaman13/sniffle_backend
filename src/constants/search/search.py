# Text data and corresponding metadata
texts = [
    "⌨️ Health metrics AI agent which focuses chat bot only for data entry. Users can enter their quantitative data through text-based prompts.",
    "📞 health metrics AI agent which focuses on voice bot for the data entry. Users can enter their quantitative data through voice-based prompts.",
    "🤖 Health metrics AI agent which focuses chat bot only for data entry. Users can enter their qualitative data through text-based prompts.",
    "📞 health metrics AI agent which focuses on voice bot for the data entry. Users can enter their qualitative data through voice-based prompts.",
    "📃 FHIR tool. An AI agent to convert image into text. Users can upload their image and get FHIR data format. Users can export the data with healthcare coach.",
    "📈 Graphs on the health data. Collections of graphs generated through the healthcare agents on the quantitative data.",
    "🪪 Summary of the health data. A summary of the health data generated by the healthcare agents.",
    "🎉 Recommendation of the health data generated by the healthcare agents. Users get recommendation on what are the steps to be taken to improve their health",
    "📲 Wearable devices. An AI agent to connect wearable devices to the healthcare agents. Users can connect their wearable devices to the healthcare agents.",
    "👨🏼‍⚕️ A general healthcare agent which is focused on answering specialized healthcare topics through chat-based interface. User can ask questions to get general knowledge of healthcare data through chat based conversation.",
    "🥼 A general healthcare agent which is focused on answering specialized healthcare topics through voice-based interface. User can ask questions to get general knowledge of healthcare data through voice based conversation.",
    "📈 About page describing how the data collection module works over the App.",
    "🦜  About page describing how the general conversation agent works in the application.",
    "⚒️ About page describing how the different tools works in the app like FHIR tool.",
]

metadata = [
    {
        "screen": "Chat",
        "intent": True,
        "chatVariant": "Health metrics agent",
        "agent_id": "health_metrics",
        "agent_type": "chat",
    },
    {
        "screen": "Voice",
        "intent": True,
        "chatVariant": "Voice health metrics agent",
        "agent_id": "voice_health_metrics",
        "agent_type": "voice",
    },
    {
        "screen": "Chat",
        "intent": True,
        "chatVariant": "Voice assessment agent",
        "agent_id": "assessment",
        "agent_type": "chat",
    },
    {
        "screen": "Voice",
        "intent": True,
        "chatVariant": "Voice assessment agent",
        "agent_id": "voice_assessment",
        "agent_type": "voice",
    },
    {"screen": "Fhir", "intent": False},
    {"screen": "Data", "intent": False},
    {"screen": "Assessment", "intent": False},
    {"screen": "Recommendations", "intent": False},
    {"screen": "Wearable", "intent": False},
    {
        "screen": "Chat",
        "intent": True,
        "chatVariant": "General Chat agent",
        "agent_id": "general_chat_response",
        "agent_type": "chat",
    },
    {
        "screen": "Voice",
        "intent": True,
        "chatVariant": "General voice agent",
        "agent_id": "general_voice_response",
        "agent_type": "voice",
    },
    {
        "screen": "About Data Collection",
        "intent": True,
        "chatVariant": "General voice agent",
        "agent_id": "general_voice_response",
        "agent_type": "voice",
    },
    {
        "screen": "About our general conversation agent",
        "intent": True,
        "chatVariant": "General voice agent",
        "agent_id": "general_voice_response",
        "agent_type": "voice",
    },
    {
        "screen": "About our tools",
        "intent": True,
        "chatVariant": "General voice agent",
        "agent_id": "general_voice_response",
        "agent_type": "voice",
    },
]
