# GPT Document Analysis Tool

## Overview

This powerful document analysis tool leverages OpenAI's advanced language models to perform comprehensive text analysis. It provides in-depth verification and analysis capabilities across multiple dimensions, including:

- Factual Accuracy Verification
- Source Verification
- Detail Verification
- Technical Detail Verification

## Features

- Supports multiple analysis types
- Utilizes GPT-4 for advanced, comprehensive analysis
- Detailed token usage tracking
- Robust error handling
- Flexible configuration options

## Prerequisites

- Python 3.8+
- OpenAI API Key
- Internet Connection

## Installation

1. Clone the repository:
```bash
git clone https://nathe444.com/nathe444/document-verification.git
cd document-verification
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate 
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the project root with your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### Available Prompt Types
- `factual_accuracy_verification`
- `source_verification`
- `detail_verification`
- `technical_detail_verification`

## Configuration Options

### OpenAIHandler Parameters
- `max_tokens`: Maximum response length 
- `model`: OpenAI model to use 
- `temperature`: Creativity of the response 

## Token Usage

The tool provides methods to track API token usage:
- `get_total_tokens_used()`: Returns total tokens used
- `reset_token_usage()`: Resets token usage counter

## Security Considerations

- Never commit your `.env` file to version control
- Use environment variables for sensitive information
- Be aware of OpenAI API usage costs

## Performance Tips

- Use caching for repeated analyses
- Monitor token usage to manage API costs
- Choose appropriate model based on your specific use case

## Troubleshooting

### Common Issues
- **API Key Not Found**: Ensure `.env` file is correctly configured
- **Rate Limiting**: The tool has built-in retry mechanisms
- **High Costs**: Monitor token usage and choose appropriate model

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

**Note**: This tool requires an active OpenAI API subscription. Usage is subject to OpenAI's terms of service and pricing.
