# ECG Signal Compression app

This web application compresses an ECG signal. The web app only accepts .bin files uploaded by the user, and uses Huffman Coding as the compression algorithm.
## Tech Stack
- Python
- Flask
- HTML/CSS
- JavaScript

## Design Considerations and Key Decisions
In designing this webapp, I wanted to keep the app as simple as possible and focus on the lossless compression algorithm, because the compression feature is the core feature of the app.

To keep the app lightweight and efficient, I chose Python for its scripting capabilities and its rich set of libraries. I chose to use Flask as the web framework to easily set up the server, quickly handle requests, and render simple HTML templates.

To keep the app simple, I was looking for a lossless compression algorithm that is simple and easy to implement. It also needed a positive compression ratio that could noticeably compress the .bin file. I don't have much experience in the compression algorithm space, so I first dived into Huffman coding. From my research reading articles, watching [youtube videos](https://youtu.be/co4_ahEDCho?si=eO9NHG4ma_fjAHpb), and other resources, I saw the benefits of Huffman Coding for compressing data and messages. The algorithm is simple, easy to implement, and efficient.
## Installation Steps
1. Clone this repository onto your local machine

        git clone https://github.com/kszeto1/flask-bin-ecg-compress-app.git
2. Create a virtual environment (optional but highly recommended)

        python3 -m venv venv
3. Activate the virtual environment
    
        source venv/bin/activate
4. Install the required dependencies

        pip install -r requirements.txt
5. Set the FLASK_APP environment variable and start the app

        set FLASK_APP=app.py && flask run
6. Open the app in your browser at http://127.0.0.1:5000/

## Huffman Coding Algorithm Implementation

1. Calculate Frequency: Count the frequency of each symbol in the input data.
2. Build a Priority Queue: Use a min-heap priority queue to store nodes of the Huffman tree based on their frequency.
3. Build the Huffman Tree: Merge nodes until there is only one node left in the priority queue. This node is the root of the Huffman tree.
4. Generate Codes: Traverse the Huffman tree to generate binary codes for each symbol.
5. Encode Data: Replace each symbol in the input data with its corresponding Huffman code.
6. (optional) Decode Data: Use the Huffman tree to decode the encoded data back to the original data.