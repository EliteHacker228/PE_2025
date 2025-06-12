import { useState } from 'react'
import { FilePicker } from './components/FilePicker'
import { ProcessingIndicator } from './components/ProcessingIndicator'
import { DownloadReady } from './components/DownloadReady'
import "./App.css"

export function App() {
  const [file, setFile] = useState<File | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [isReady, setIsReady] = useState(false)

  const handleFileSelect = (selectedFile: File) => {
    setFile(selectedFile)
    setIsProcessing(true)
    setIsReady(false)

    // Эмулируем обработку
    setTimeout(() => {
      setIsProcessing(false)
      setIsReady(true)
    }, 3000)
  }

  const handleDownload = () => {
    alert('Скачивание файла...')
  }

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <div className="title">
        <h1 className="main__title">ORIENTED OBJECT DETECTION FOR TABLE RECOGNITION</h1>
        <p className="main__subtitle">Распознование таблицы и угла наклона.</p>
      </div>
      <div className="main_function">
        <h2 className="main_function__title">Обработка файла</h2>

        {!file && <FilePicker onFileSelect={handleFileSelect} />}
        {file && !isProcessing && !isReady && (
          <p>Файл выбран: <strong>{file.name}</strong></p>
        )}
        {isProcessing && <ProcessingIndicator />}
        {isReady && <DownloadReady onDownload={handleDownload} />}
      </div>
    </div>
  )
}
