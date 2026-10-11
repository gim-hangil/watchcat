# watchcat

__`watchcat`__ is safety watchdog &mdash; but it's a __*cat*__.

## Requirements

* `uv` for managing python environment
* `node` for building frontend

> The other dependencies will be installed during deployment using `uv` and
  `npm`.

## Deployment

```sh
# Clone this repository
git clone https://github.com/gim-hangil/watchcat
cd watchcat

# Build Vue.js application
cd web
npm install
npm run build

# Run the server for API and frontend
cd ../api
uv sync
uv run fastapi dev
```

Now the server is running at `http://localhost:8000`.

> This instructions are for development usage.
