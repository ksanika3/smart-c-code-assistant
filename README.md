# C Programming Assistant

A Streamlit-based web application that helps users learn and generate C programming code using Google's Gemini AI model.

## Features

- **User Authentication**: Secure login and signup system
- **AI Code Generation**: Generate C code snippets using Gemini AI
- **Interactive Chat Interface**: User-friendly chat interface for code requests
- **Syntax Highlighting**: Clean code display with proper syntax highlighting
- **Modern UI**: Responsive and clean user interface

## Prerequisites

- Python 3.10 or higher
- Streamlit
- SQLite3
- Google Gemini API key

## Installation

1. Clone the repository or download the files to your local machine

2. Install the required packages:
```bash
pip install streamlit requests python-dotenv
```

3. Create a `.env` file in the project root directory and add your Gemini API key:
```
GEMINI_API_KEY=your_actual_api_key_here
```

To get your API key:
- Visit https://makersuite.google.com/app/apikey
- Create a new API key
- Copy and paste it in the `.env` file

## Running the Application

1. Open a terminal in the project directory
2. Run the following command:
```bash
streamlit run new_trail.py
```
3. The application will open in your default web browser

## Usage

1. **Sign Up**:
   - Click the "Sign Up" button
   - Enter your desired username and password
   - Confirm your password
   - Click "Sign Up"

2. **Login**:
   - Enter your username and password
   - Click "Login"

3. **Generate Code**:
   - Type your C programming question or request in the chat input
   - Press Enter or click the send button
   - The AI will generate appropriate C code
   - Use the "Copy Code" button to copy the generated code

4. **Navigation**:
   - Use the top navigation buttons to switch between pages
   - Click "Logout" when you're done

## Project Structure

- `new_trail.py`: Main application file
- `database.py`: Database handling and user authentication
- `.env`: Configuration file for API keys
- `chat_app.db`: SQLite database file (auto-generated)

## Troubleshooting

1. **API Key Error**:
   - Make sure you have created the `.env` file
   - Verify your API key is correct
   - Restart the application after adding the API key

2. **Database Issues**:
   - If you encounter database errors, delete `chat_app.db` and restart the application
   - The database will be automatically recreated with the correct schema

3. **Streamlit Not Found**:
   - Reinstall Streamlit: `pip install streamlit --force-reinstall`
   - Make sure Python is in your system PATH

## Security Notes

- Passwords are hashed before storage
- API keys are stored securely in `.env` file
- Database uses SQLite with proper security measures
- Session management is handled securely

## Contributing

Feel free to fork this project and submit pull requests for any improvements.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Google Gemini API for providing the AI capabilities
- Streamlit for the web interface framework
- The open-source community for various dependencies 