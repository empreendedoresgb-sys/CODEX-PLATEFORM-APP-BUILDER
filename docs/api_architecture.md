# API Architecture Draft

## Base URL
`https://api.apbuilder.app/v1/`

## Endpoints
- `GET /languages`
- `POST /generate/text`
- `POST /generate/multilingual`
- `POST /validate`

## Flow
`User -> API -> Core -> Language Selector -> Validation -> Response`
