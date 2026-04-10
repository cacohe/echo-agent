import 'package:record/record.dart';
import 'package:path_provider/path_provider.dart';
import 'dart:io';

enum AudioState { idle, recording, processing }

class AudioService {
  final AudioRecorder _recorder = AudioRecorder();
  AudioState _state = AudioState.idle;

  AudioState get state => _state;

  Future<bool> hasPermission() async {
    return await _recorder.hasPermission();
  }

  Future<String?> startRecording() async {
    if (_state != AudioState.idle) return null;
    
    final hasPermission = await _recorder.hasPermission();
    if (!hasPermission) return null;

    final dir = await getTemporaryDirectory();
    final path = '${dir.path}/recording_${DateTime.now().millisecondsSinceEpoch}.wav';

    await _recorder.start(
      RecordConfig(encoder: AudioEncoder.wav),
      path: path,
    );

    _state = AudioState.recording;
    return path;
  }

  Future<String?> stopRecording() async {
    if (_state != AudioState.recording) return null;

    final path = await _recorder.stop();
    _state = AudioState.processing;
    return path;
  }

  Future<void> cancelRecording() async {
    if (_state == AudioState.recording) {
      await _recorder.stop();
    }
    _state = AudioState.idle;
  }

  void setIdle() {
    _state = AudioState.idle;
  }

  Future<void> dispose() async {
    await _recorder.dispose();
  }
}
