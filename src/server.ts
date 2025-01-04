import http from "http";
import app from "./app";
import { error } from "console";

const PORT = process.env.PORT || 4000;

const server = http.createServer(app);

server.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});

server.on('error', (error: NodeJS.ErrnoException) => {
    console.error("Server error: ", error.message);
    process.exit(1);
});