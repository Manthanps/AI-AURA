import Foundation
import AppKit
import ApplicationServices
import CoreGraphics

// Wrapper: allow single-file command `swift swift_controller.swift`
// This re-invokes Swift with the other source files included.
let env = ProcessInfo.processInfo.environment
if env["SWIFT_CHILD"] != "1" {
    let process = Process()
    process.executableURL = URL(fileURLWithPath: "/usr/bin/swift")
    process.arguments = [
        "swift_controller.swift",
        "vision_ocr.swift",
        "ui_automation.swift"
    ]
    var newEnv = env
    newEnv["SWIFT_CHILD"] = "1"
    process.environment = newEnv
    process.currentDirectoryURL = URL(fileURLWithPath: FileManager.default.currentDirectoryPath)
    try? process.run()
    process.waitUntilExit()
    exit(process.terminationStatus)
}

// Paths
let baseDir = FileManager.default.currentDirectoryPath
let shotsDir = baseDir + "/screenshots"
let screenshotPath = shotsDir + "/screen.png"
let pythonPath = "/usr/bin/python3"
let pythonScript = baseDir + "/python_ocr.py"
let minConfidence: Float = 0.65

// Ensure screenshots directory exists
try? FileManager.default.createDirectory(atPath: shotsDir, withIntermediateDirectories: true)

// Capture full screen as PNG
func captureScreenPNG(to path: String) {
    let displayID = CGMainDisplayID()
    guard let image = CGDisplayCreateImage(displayID) else { return }
    let bitmap = NSBitmapImageRep(cgImage: image)
    guard let data = bitmap.representation(using: .png, properties: [:]) else { return }
    try? data.write(to: URL(fileURLWithPath: path))
}

// Open a macOS app (example: Safari) to demonstrate workflow
func openApp(named name: String) {
    NSWorkspace.shared.launchApplication(name)
}

// Main workflow
openApp(named: "Safari")

// Give the app a moment to focus
Thread.sleep(forTimeInterval: 1.0)

captureScreenPNG(to: screenshotPath)

let ocr = combinedOCR(
    imagePath: screenshotPath,
    pythonPath: pythonPath,
    pythonScript: pythonScript,
    minConfidence: minConfidence
)

let keywords = ["login", "submit", "next", "cancel"]
let textLower = ocr.text.lowercased()
let shouldClick = keywords.first { textLower.contains($0) }

if let kw = shouldClick {
    print("Detected keyword: \(kw)")
    if let app = focusedApplication(),
       let button = findButtonByKeywords(app, keywords: [kw]) {
        if clickAXElement(button) {
            print("Clicked button: \(kw)")
        } else {
            print("Failed to click button")
        }
    } else {
        print("Button not found via accessibility")
    }
} else {
    print("No keywords detected")
}
