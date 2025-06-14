import { useState, useEffect } from 'react'
import { FilePicker } from './components/FilePicker'
import { ProcessingIndicator } from './components/ProcessingIndicator'
import { DownloadReady } from './components/DownloadReady'
import "./App.css"

export function App() {
  const [file, setFile] = useState<File | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [isReady, setIsReady] = useState(false)
  const [downloadUrl, setDownloadUrl] = useState<string | null>(null)

  const handleFileSelect = (selectedFile: File) => {
    setFile(selectedFile)
    setIsProcessing(false)
    setIsReady(false)
    setDownloadUrl(null)
  }

  const handleProcess = async () => {
    if (!file) return

    setIsProcessing(true)
    setIsReady(false)
    setDownloadUrl(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('http://localhost:8000/detect-rotate/', {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        throw new Error('Ошибка при обработке файла')
      }

      const blob = await response.blob()
      const url = URL.createObjectURL(blob)
      setDownloadUrl(url)
      setIsReady(true)
    } catch (error) {
      console.error('Ошибка загрузки:', error)
    } finally {
      setIsProcessing(false)
    }
  }

  const handleReset = () => {
    if (downloadUrl) {
      URL.revokeObjectURL(downloadUrl)
    }
    setFile(null)
    setIsProcessing(false)
    setIsReady(false)
    setDownloadUrl(null)
  }

  useEffect(() => {
    return () => {
      if (downloadUrl) {
        URL.revokeObjectURL(downloadUrl)
      }
    }
  }, [downloadUrl])

  return (
    <div>
      <div className="title">
        <h1 className="main-title">ORIENTED OBJECT DETECTION FOR TABLE RECOGNITION</h1>
        <p className="main-subtitle">Распознование таблицы и угла наклона.</p>
      </div>
      <div className="main-function">
        <h2 className="main-function-title">Обработка файла</h2>

        {!file && <FilePicker onFileSelect={handleFileSelect} />}

        {file && !isProcessing && !isReady && (
          <div>
            <p>Файл выбран: <strong>{file.name}</strong></p>
            <button className="file-button pick-button process-button" onClick={handleProcess}>
              Обработать
            </button>
            <button className="file-button other-button reset-button" onClick={handleReset}>
              Выбрать другой файл
            </button>
          </div>
        )}

        {isProcessing && <ProcessingIndicator />}

        {isReady && downloadUrl && file && (
          <div>
            <DownloadReady downloadUrl={downloadUrl} filename={`processed_${file.name}`} />
            <button className="file-button other-button reset-button" onClick={handleReset}>
              Выбрать другой файл
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
