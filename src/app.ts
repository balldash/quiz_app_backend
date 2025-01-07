import express, { Application, Request, Response, NextFunction } from 'express';
import morgan from "morgan";
import helmet from "helmet";
import cors from "cors";
import dotenv from "dotenv";
import routes from "./routes";

dotenv.config();

const app: Application = express();

app.use(morgan("dev"));
app.use(helmet());
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use("/api", routes);

app.get("/", (req: Request, res: Response) => {
    res.status(200).send({ message: "API is running!" });
});

app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
    console.error(err.stack);
    res.status(500).send({error: "Something went wrong!"});
});

export default app;