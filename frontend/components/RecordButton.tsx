"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { VoiceRecorder } from "./VoiceRecorder";

interface RecordButtonProps {
  onRecordCreated?: () => void;
}

export function RecordButton({ onRecordCreated }: RecordButtonProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [showRecorder, setShowRecorder] = useState(false);

  const handleStartRecording = () => {
    setIsRecording(true);
    setShowRecorder(true);
  };

  const handleStopRecording = () => {
    setIsRecording(false);
  };

  const handleClose = () => {
    setShowRecorder(false);
    setIsRecording(false);
  };

  return (
    <>
      <motion.button
        onClick={handleStartRecording}
        className="w-32 h-32 rounded-full bg-primary shadow-lg flex items-center justify-center"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <svg
          className="w-12 h-12 text-white"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"
          />
        </svg>
      </motion.button>

      {showRecorder && (
        <VoiceRecorder
          onClose={handleClose}
          onStop={handleStopRecording}
          onRecordCreated={onRecordCreated}
        />
      )}
    </>
  );
}