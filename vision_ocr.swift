import Foundation
import Vision
import AppKit

// OCR result container
struct OCRResult {
    let text: String
    let confidence: Float
}

// Run Vision OCR on an image at a given URL
func visionOCR(imageURL: URL) -> OCRResult {
    guard let image = NSImage(contentsOf: imageURL),
          let tiff = image.tiffRepresentation,
          let bitmap = NSBitmapImageRep(data: tiff),
          let cgImage = bitmap.cgImage else {
        return OCRResult(text: "", confidence: 0.0)
    }

    let request = VNRecognizeTextRequest()
    request.recognitionLevel = .accurate
    request.usesLanguageCorrection = true

    let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
    do {
        try handler.perform([request])
    } catch {
        return OCRResult(text: "", confidence: 0.0)
    }

    var lines: [String] = []
    var confidences: [Float] = []
    let observations = request.results as? [VNRecognizedTextObservation] ?? []
    for obs in observations {
        if let top = obs.topCandidates(1).first {
            lines.append(top.string)
            confidences.append(top.confidence)
        }
    }
    let avg = confidences.isEmpty ? 0.0 : confidences.reduce(0, +) / Float(confidences.count)
    return OCRResult(text: lines.joined(separator: "\n"), confidence: avg)
}

// Fallback OCR via Python script using Process
func pythonOCR(pythonPath: String, scriptPath: String, imagePath: String) -> OCRResult {
    let process = Process()
    process.executableURL = URL(fileURLWithPath: pythonPath)
    process.arguments = [scriptPath, imagePath]

    let pipe = Pipe()
    process.standardOutput = pipe
    process.standardError = Pipe()

    do {
        try process.run()
        process.waitUntilExit()
    } catch {
        return OCRResult(text: "", confidence: 0.0)
    }

    let data = pipe.fileHandleForReading.readDataToEndOfFile()
    let text = String(data: data, encoding: .utf8) ?? ""
    return OCRResult(text: text.trimmingCharacters(in: .whitespacesAndNewlines), confidence: 0.0)
}

// Combined OCR: Vision first, fallback to Python if confidence is low
func combinedOCR(imagePath: String, pythonPath: String, pythonScript: String, minConfidence: Float) -> OCRResult {
    let vision = visionOCR(imageURL: URL(fileURLWithPath: imagePath))
    if vision.confidence >= minConfidence && !vision.text.isEmpty {
        return vision
    }
    return pythonOCR(pythonPath: pythonPath, scriptPath: pythonScript, imagePath: imagePath)
}
