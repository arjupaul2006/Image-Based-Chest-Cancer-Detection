import { useEffect, useState } from "react";
import "./App.css";
import axios from "axios";

function App() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState("");
  const [result, setResult] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  useEffect(() => {
    return () => {
      if (preview) URL.revokeObjectURL(preview);
    };
  }, [preview]);

  const handleImageChange = (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setImage(file);
    setPreview(URL.createObjectURL(file));
    setResult(null);
  };

  const analyzeImage = async () => {
    if (!image) return;

    setIsAnalyzing(true);

    try {
      const formData = new FormData();
      formData.append("file", image);

      const response = await axios.post(
        `${import.meta.env.VITE_BACKEND_URL}/predict`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        },
      );

      setResult(response.data);
    } catch (error) {
      console.error("Error analyzing image:", error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <main className="min-h-screen bg-black text-white">
      <nav className="flex w-full items-center justify-between px-6 py-6">
        <div className="flex items-center gap-3">
          <div className="rounded-xl bg-yellow-400 p-2 text-black">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path
                d="M12 21s-7-4.35-9.5-9.05C.36 7.72 2.8 4 6.5 4c2.1 0 3.65 1.18 4.5 2.62C11.85 5.18 13.4 4 15.5 4c3.7 0 6.14 3.72 4 7.95C19 16.65 12 21 12 21Z"
                stroke="currentColor"
                strokeWidth="1.8"
              />
            </svg>
          </div>
          <span className="text-xl font-bold">LungVision</span>
        </div>
        <span className="hidden rounded-full border border-slate-700 px-4 py-2 text-sm text-slate-300 sm:block">
          AI-assisted screening
        </span>
      </nav>

      <section className="w-full px-6 pb-16 pt-10">
        <div className="mb-12 max-w-3xl">
          <p className="mb-4 font-semibold uppercase tracking-[0.25em] text-yellow-400">
            Chest image analysis
          </p>
          <h1 className="text-4xl font-bold leading-tight sm:text-6xl">
            Detect risks earlier with intelligent imaging.
          </h1>
          <p className="mt-6 text-lg leading-8 text-slate-400">
            Upload a chest X-ray image to receive an AI-generated prediction and
            confidence score in seconds.
          </p>
        </div>

        <div className="grid w-full gap-8 lg:grid-cols-2">
          <section className="rounded-3xl border border-zinc-800 bg-zinc-950 p-6 shadow-2xl sm:p-8">
            <div className="mb-6 flex items-center justify-between">
              <div>
                <h2 className="text-xl font-semibold">Upload an image</h2>
                <p className="mt-1 text-sm text-slate-400">
                  PNG, JPG, or JPEG up to 10 MB
                </p>
              </div>
              <span className="rounded-full bg-yellow-400/10 px-3 py-1 text-xs font-medium text-yellow-300">
                Secure
              </span>
            </div>

            <label
              htmlFor="image-upload"
              className="group flex min-h-80 cursor-pointer flex-col items-center justify-center overflow-hidden rounded-2xl border-2 border-dashed border-zinc-700 bg-black/70 transition hover:border-yellow-400"
            >
              {preview ? (
                <img
                  src={preview}
                  alt="Selected chest scan"
                  className="h-80 w-full object-contain"
                />
              ) : (
                <>
                  <div className="mb-4 rounded-2xl bg-yellow-400/10 p-4 text-yellow-400">
                    <svg width="36" height="36" viewBox="0 0 24 24" fill="none">
                      <path
                        d="M12 16V4m0 0L8 8m4-4 4 4M5 14v3a3 3 0 0 0 3 3h8a3 3 0 0 0 3-3v-3"
                        stroke="currentColor"
                        strokeWidth="1.8"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      />
                    </svg>
                  </div>
                  <p className="font-semibold">Click to upload your scan</p>
                  <p className="mt-2 text-sm text-slate-500">
                    or drag and drop an image here
                  </p>
                </>
              )}
              <input
                id="image-upload"
                type="file"
                accept="image/png,image/jpeg,image/jpg, image/jfif, image/webp, image/avif"
                onChange={handleImageChange}
                className="hidden"
              />
            </label>

            <button
              onClick={analyzeImage}
              disabled={!image || isAnalyzing}
              className="mt-6 w-full rounded-xl bg-yellow-400 px-5 py-3.5 font-bold text-black transition hover:bg-yellow-300 disabled:cursor-not-allowed disabled:opacity-40"
            >
              {isAnalyzing ? "Analyzing image..." : "Analyze image"}
            </button>
          </section>

          <section className="rounded-3xl border border-zinc-800 bg-zinc-950 p-6 sm:p-8">
            <h2 className="text-xl font-semibold">Prediction result</h2>
            <p className="mt-1 text-sm text-slate-400">
              Results will appear here after analysis.
            </p>

            {!result ? (
              <div className="mt-8 flex min-h-64 flex-col items-center justify-center rounded-2xl bg-black/60 text-center">
                <div className="mb-4 rounded-full bg-slate-800 p-4 text-slate-500">
                  <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
                    <path
                      d="M12 8v4m0 4h.01M10.3 3.3 2.7 18a2 2 0 0 0 1.75 3h15.1a2 2 0 0 0 1.75-3L13.7 3.3a2 2 0 0 0-3.4 0Z"
                      stroke="currentColor"
                      strokeWidth="1.8"
                      strokeLinecap="round"
                    />
                  </svg>
                </div>
                <p className="text-slate-400">No analysis available yet</p>
              </div>
            ) : (
              <div className="mt-8">
                <div className="rounded-2xl border border-emerald-400/20 bg-emerald-400/10 p-5">
                  <p className="text-sm text-emerald-300">Model prediction</p>
                  <h3 className="mt-2 text-2xl font-bold text-emerald-200">
                    {result.predicted_class}
                  </h3>
                </div>

                <div className="mt-6">
                  <div className="mb-2 flex justify-between text-sm">
                    <span className="text-slate-400">Confidence score</span>
                    <strong>{result.confidence}%</strong>
                  </div>
                  <div className="h-3 overflow-hidden rounded-full bg-slate-800">
                    <div
                      className="h-full rounded-full bg-yellow-400"
                      style={{ width: `${result.confidence}%` }}
                    />
                  </div>
                </div>

                <p className="mt-6 text-sm leading-6 text-slate-500">
                  This AI result is for screening support only and is not a
                  medical diagnosis. Please consult a qualified healthcare
                  professional.
                </p>
              </div>
            )}
          </section>
        </div>
      </section>
    </main>
  );
}

export default App;
