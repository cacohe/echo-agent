"use client";

import { useState, useEffect, useRef } from "react";
import { motion } from "framer-motion";
import { apiClient } from "@/lib/api";

interface VoiceRecorderProps {
  onClose: () => void;
  onStop: () => void;
  onRecordCreated?: () => void;
}

export function VoiceRecorder({ onClose, onStop, onRecordCreated }: VoiceRecorderProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [duration, setDuration] = useState(0);
  const [transcript, setTranscript] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);
  const recognitionRef = useRef<SpeechRecognition | null>(null);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    if (typeof window !== "undefined" && ("SpeechRecognition" in window || "webkitSpeechRecognition" in window)) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = true;
      recognitionRef.current.interimResults = true;
      recognitionRef.current.lang = "zh-CN";

      recognitionRef.current.onresult = (event) => {
        let finalTranscript = "";
        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            finalTranscript += transcript;
          }
        }
        if (finalTranscript) {
          setTranscript((prev) => prev + finalTranscript);
        }
      };

      recognitionRef.current.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
      };
    }

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, []);

  const startRecording = () => {
    if (recognitionRef.current) {
      recognitionRef.current.start();
    }
    setIsRecording(true);
    timerRef.current = setInterval(() => {
      setDuration((d) => d + 1);
    }, 1000);
  };

  const stopRecording = async () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
    if (timerRef.current) {
      clearInterval(timerRef.current);
    }
    setIsRecording(false);
    setIsProcessing(true);

    const text = transcript || "语音记录";

    try {
      await apiClient.createRecord({
        content: text,
        type: "voice",
      });
      onRecordCreated?.();
    } catch (error) {
      console.error("Failed to create record:", error);
    }

    setIsProcessing(false);
    onStop();
    onClose();
  };

  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
      onClick={onClose}
    >
      <motion.div
        initial={{ scale: 0.95 }}
        animate={{ scale: 1 }}
        className="bg-surface rounded-lg p-6 m-4 max-w-sm w-full"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold text-text-primary">录音中</h2>
          <button onClick={onClose} className="text-text-secondary">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div className="flex flex-col items-center">
          <motion.div
            animate={isRecording ? { scale: [1, 1.1, 1] } : {}}
            transition={{ repeat: Infinity, duration: 1 }}
            className={`w-20 h-20 rounded-full ${isRecording ? "bg-accent" : "bg-primary"} flex items-center justify-center mb-4`}
          >
            <svg className="w-10 h-10 text-white" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" />
              <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
            </svg>
          </motion.div>

          <p className="text-2xl font-mono mb-4">{formatDuration(duration)}</p>

          {transcript && (
            <div className="w-full bg-primary-light rounded-lg p-3 mb-4 max-h-32 overflow-y-auto">
              <p className="text-sm text-text-primary">{transcript}</p>
            </div>
          )}

          <div className="flex gap-4">
            {!isRecording ? (
              <motion.button
                whileTap={{ scale: 0.95 }}
                onClick={startRecording}
                className="px-6 py-2 bg-primary text-white rounded-full"
              >
                开始录音
              </motion.button>
            ) : (
              <motion.button
                whileTap={{ scale: 0.95 }}
                onClick={stopRecording}
                disabled={isProcessing}
                className="px-6 py-2 bg-accent text-white rounded-full disabled:opacity-50"
              >
                {isProcessing ? "处理中..." : "停止"}
              </motion.button>
            )}
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}