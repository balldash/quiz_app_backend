import { Router, Request, Response } from "express";

const router = Router();

router.get("/quizzes", (req: Request, res: Response) => {
    res.status(200).send({ message: "List of quizzes" });
});

router.post("/quizzes", (req: Request, res: Response) => {
    const { title, questions } = req.body;
    res.status(201).send({ message: "Quiz created", data: { title: questions } });
});

export default router;