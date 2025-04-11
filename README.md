# jenkins-user-dumper 🔍

A Python tool to extract user information from unauthenticated Jenkins dashboards.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Features ✨
- IP/Domain target input
- JSON API endpoint scraping
- Dynamic timeout configuration
- Colored console output
- Result export to file
- Debug mode for raw JSON inspection

## Installation ⚙️
```bash
git clone https://github.com/yourusername/jenkins-user-dumper.git
cd jenkins-user-dumper
pip install -r requirements.txt
```

## Usage 🚀
```bash
# Basic usage with domain
python jenkins_users.py -d example.com -o users.txt

# With IP and port
python jenkins_users.py -i 192.168.1.100 -p 8080 -t 15

# Enable debug mode
python jenkins_users.py -d jenkins.example.com --debug
```

## Command Line Options 📋
| Option | Description |
|--------|-------------|
| `-i/--ip` | Target IP address |
| `-p/--port` | Target port number |
| `-d/--domain` | Target domain name |
| `-o/--output` | Output file name |
| `-t/--timeout` | Request timeout in seconds (default: 10) |
| `--debug` | Show raw JSON response |
| `-h/--help` | Show help message |

## Contributing 🤝
1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License 📄
Distributed under the MIT License. See `LICENSE` for more information.
