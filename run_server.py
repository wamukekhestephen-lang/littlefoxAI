#!/usr/bin/env python3
import sys
import os
from app import app

if __name__ == '__main__':
    # Force single-threaded to avoid threading issues
    port = int(os.environ.get('PORT', 5000))
    print(f"\n[INFO] Starting Flask on 127.0.0.1:{port}...", file=sys.stderr)
    
    try:
        app.run(
            host='127.0.0.1',
            port=port,
            debug=False,
            use_reloader=False,
            threaded=False
        )
    except Exception as e:
        print(f"[ERROR] Failed to start Flask: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
