from flask import Flask, request, jsonify, send_file
from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
from dashscope import ImageSynthesis
import os

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate_image():
    data = request.json
    prompt = data.get('prompt')
    negative_prompt = data.get('negative_prompt')
    api_key = data.get('api_key', 'sk-7c3ad80f4f47499abeaaf2ff81c51c54')

    if not prompt:
        return jsonify({'error': '缺少提示词参数'}), 400

    try:
        rsp = ImageSynthesis.call(
            api_key=api_key,
            model="wanx2.1-t2i-turbo",
            prompt=prompt,
            negative_prompt=negative_prompt if negative_prompt else None,
            n=3,
            size='1024*1024'
        )

        if rsp.status_code == HTTPStatus.OK:
            results = [{'url': result.url} for result in rsp.output.results]
            return jsonify({'results': results})
        else:
            return jsonify({'error': f'生成失败: {rsp.message}'}), rsp.status_code

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return send_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)