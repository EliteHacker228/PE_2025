interface DownloadReadyProps {
    downloadUrl: string
    filename: string
}

export const DownloadReady: React.FC<DownloadReadyProps> = ({ downloadUrl, filename }) => {
    return (
        <div className="download-ready">
            <p>Файл готов!</p>
            <a href={downloadUrl} download={filename}>
                <button data-testid="down-file" className="file-button pick-button reset-button">Скачать готовый файл</button>
            </a>
        </div>
    )
}