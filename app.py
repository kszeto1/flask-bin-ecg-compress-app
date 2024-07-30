from flask import Flask, request, send_file, render_template, jsonify
import heapq
from collections import Counter

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Implement Huffman coding algorithm

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other): #allows comparison between nodes based on frequency
        return self.freq < other.freq

# build Huffman tree based on character frequencies
def build_huffman_tree(data):
    frequency = Counter(data)
    heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged) # repeatedly merge two nodes with the lowest frequencies until only one node (root) remains

    return heap[0]

# generate Huffman codes for each character
def build_huffman_codes(root):
    codes = {}

    def traverse(node, code): #traverse Huffman tree and generate codes for each character
        if node.char is not None:
            codes[node.char] = code
            return
        traverse(node.left, code + "0") #left branches are assigned '0'
        traverse(node.right, code + "1") #right branches are assigned '1'

    traverse(root, "")
    return codes

# compress data using Huffman codes
def compress_data(data, codes):
    encoded = "".join(codes[char] for char in data) #encode input data using Huffman codes
    padding = 8 - (len(encoded) % 8) #pad encoded data to multiple of 8 bits
    encoded += "0" * padding
    compressed = bytearray()
    for i in range(0, len(encoded), 8):
        byte = encoded[i:i+8]
        compressed.append(int(byte, 2))
    return bytes(compressed), padding #convert binary string to bytes and return compressed data and padding length

@app.route('/compress', methods=['POST'])
def compress():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    data = file.read()
    original_size = len(data)

    root = build_huffman_tree(data)
    codes = build_huffman_codes(root)
    compressed_data, padding = compress_data(data, codes)
    compressed_size = len(compressed_data)

    # Calculate compression ratio
    compression_ratio = f"{(1 - compressed_size / original_size) * 100:.2f}%"

    # Save compressed data
    with open('compressed.bin', 'wb') as f:
        f.write(compressed_data)

    # Save Huffman tree
    with open('huffman_tree.txt', 'w') as f:
        f.write(str(padding) + '\n')
        for char, code in codes.items():
            f.write(f"{char}:{code}\n")

    return jsonify({
        "original_size": original_size,
        "compressed_size": compressed_size,
        "compression_ratio": compression_ratio,
        "compressed_data": compressed_data.hex()  # Convert bytes to hex string for JSON
    })

@app.route('/compression_result')
def compression_result():
    return render_template('compression_result.html',
                           original_size=request.args.get('original_size'),
                           compressed_size=request.args.get('compressed_size'),
                           compression_ratio=request.args.get('compression_ratio'))

@app.route('/download_compressed')
def download_compressed():
    return send_file('compressed.bin', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)