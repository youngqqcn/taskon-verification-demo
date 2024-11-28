# TaskOn Verification API Demo

This repository provides a demo implementation of the TaskOn Verification API. It serves as a reference for implementing your own verification service that integrates with TaskOn.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Ftaskon-xyz%2Ftaskon-verification-demo)

## Features

- FastAPI-based verification endpoint
- OpenAPI/Swagger documentation
- One-click Vercel deployment
- Demo implementation of task verification logic

## API Documentation

### Verification Endpoint

- **URL**: `/api/task/verification`
- **Method**: GET
- **Query Parameters**: 
  - `address`: Wallet address or social media ID (case-insensitive)
- **Optional Headers**:
  - `Authorization`: Bearer token (if enabled)

#### Response Format

```json
{
    "result": {
        "isValid": true|false
    }
}
```

## Local Development

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the development server:
   ```
   uvicorn api.index:app --reload
   ```

3. Access the API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Deployment

1. Click the "Deploy with Vercel" button above
2. Follow the Vercel deployment process
3. Your API will be available at your Vercel deployment URL

## Demo Implementation Details

The demo implementation includes:

- Sample verification logic
- Pre-configured test addresses
- Bearer token support
- Case-insensitive address handling

## Testing

Use the Swagger UI at `/docs` to test the API endpoints. The demo includes several pre-configured addresses for testing:

- Wallet address: `0xd5045deea369d64ab7efab41ad18b82eeabcdefg`
- Twitter handle: `taskonxyz`
- Discord ID: `1084460817220641111`
- Telegram ID: `6881505111`
- Email: `demo@taskon.xyz`

## Support

For questions or support, please refer to the TaskOn documentation or contact the TaskOn team.
