from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from collections import deque
from threading import Lock
import time

app = FastAPI()  
class RateLimiter:
    def __init__(self):
        self.user_requests = {}
        self.lock = Lock()

    def allow_request(self, user_id: str) -> bool:
        current_time = time.time()
        if user_id not in self.user_requests:
            self.user_requests[user_id] = deque()
        
        request_queue = self.user_requests[user_id]
        while request_queue and request_queue[0] < current_time - 1:
            request_queue.popleft()
        
        if len(request_queue) >= 5:
            return False
        
        request_queue.append(current_time)
        return True

limiter = RateLimiter()

@app.get("/api/request")
async def handle_request(request: Request):
    user_id = request.query_params.get("user_id", "default_user")
    if not limiter.allow_request(user_id):
        raise HTTPException(status_code=429, detail="Rate limit exceeded (5 requests/second)")
    return {"status": "allowed", "message": "Request processed successfully."}

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <body>
            <button onclick="makeRequest()">Send Request</button>
            <div id="result"></div>
            <script>
                async function makeRequest() {
                    const userId = "browser_user";
                    const response = await fetch(`/api/request?user_id=${userId}`);
                    const data = await response.ok ? await response.json() : {status: "denied", message: await response.text()};
                    document.getElementById("result").innerHTML += 
                        `<p>Status: ${data.status}, Message: ${data.message}</p>`;
                }
            </script>
        </body>
    </html>
    """