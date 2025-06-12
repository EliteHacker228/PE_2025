interface DownloadReadyProps {
    onDownload: () => void
}

export const DownloadReady: React.FC<DownloadReadyProps> = ({ onDownload }) => {
    return (
        <div>
            <p>Файл готов!</p>
            <button onClick={onDownload}>Скачать готовый файл</button>
        </div>
    )
}