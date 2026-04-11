import csv
import io
from app.utils.helper import expected_headers

class FileService:
    """
    Read and validate CSV header
    """
    @staticmethod
    def validate_header(file, header_for):
        header_line = file.readline().strip()
        print(f"Actual headers: {header_line}")
        # Convert header line to list of column names
        actual_headers = header_line.split(",")
        # Get expected headers for the given header_for key
        EXPECTED_HEADERS = expected_headers(header_for)

        # if actual_headers != EXPECTED_HEADERS:
        #     raise HTTPException(
        #         status_code=400,
        #         detail=f"Invalid header. Expected {EXPECTED_HEADERS}, got {actual_headers}"
        #     )

        return actual_headers
    
    """
    Count total rows in CSV using binary chunks (fastest method)
    Assumes 1 row = 1 newline (\n)
    """
    def count_rows_binary(upload_file, chunk_size=1024 * 1024):
        file = upload_file.file

        total_lines = 0
        last_char = b""

        try:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break

                total_lines += chunk.count(b"\n")
                last_char = chunk[-1:]  # track last byte

            # If file doesn't end with newline, count last line
            if last_char != b"\n":
                total_lines += 1

            # Subtract header
            total_rows = max(total_lines - 1, 0)

            return total_rows

        finally:
            # 🔥 VERY IMPORTANT → reset file pointer
            file.seek(0)

    """
    Read CSV file and yield each line as a dictionary
    """
    @staticmethod
    def read_file(file):
        file_name = file.filename
        uploaded_file = file.file
         # ✅ Convert bytes → text stream
        text_file = io.TextIOWrapper(
            uploaded_file, 
            encoding="utf-8",
            newline=""   # important for csv correctness
        )
        #Stream CSV file safely with header validation
        headers = FileService.validate_header(text_file, header_for="USER")
        # CSV Reader (continues after header)
        reader = csv.DictReader(text_file, fieldnames=headers)

        for row_number, row in enumerate(reader, start=2):
            try:
                # Clean row (strip spaces, handle None)
                cleaned_row = {
                    k: v.strip() if isinstance(v, str) else v
                    for k, v in row.items()
                }

                # Skip empty rows
                if not any(cleaned_row.values()):
                    continue

                yield cleaned_row

            except Exception as e:
                logger.error(f"[ROW ERROR] Row {row_number}: {e}")
                continue