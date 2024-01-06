import { useState } from "react";
import { pipeline } from "@xenova/transformers";
import "./App.css";

function App() {
  const [input, setInput] = useState("Insert text here");
  const [output, setOutput] = useState("");

  const classify = async () => {
    const classifier = await pipeline(
      "text-classification",
      "Xenova/distilbert-base-uncased-finetuned-sst-2-english"
    );
    const analysis = await classifier(input);

    const label = analysis[0].label;
    const labelEmoji = label === "POSITIVE" ? "😊" : "😔";
    const score = Math.round(100 * analysis[0].score);
    setOutput(label + " " + labelEmoji + " " + score + "%");
  };

  return (
    <>
      <h1>Sentiment Analysis 💔</h1>
      <h3>Download AI models and classify text on your browser!</h3>
      <textarea value={input} onChange={(e) => setInput(e.target.value)} />
      <br />
      <button onClick={classify}>Go!</button>
      <h2>{output}</h2>
    </>
  );
}

export default App;
