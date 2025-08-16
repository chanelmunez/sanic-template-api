export async function GET() {
  return Response.json({
    status: "healthy",
    message: "Next.js API is running",
    version: "1.0.0"
  });
}
