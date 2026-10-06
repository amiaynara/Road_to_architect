"""simplest_db.sh, ported to Python, plus an in-memory hash index.

Same on-disk format as chapter3/database: one `key,value` per line, appended.
The index maps key -> byte offset of that key's latest line in the file.
"""

import os


def encode(key: str, value: str) -> bytes:
    return f"{key},{value}\n".encode()


def decode(line: bytes) -> tuple[str, str]:
    key, _, value = line.decode().rstrip("\n").partition(",")
    return key, value


class HashIndexDB:
    def __init__(self, path: str):
        self.path = path
        open(path, "ab").close()          # create the file if missing
        self._writer = open(path, "ab")   # append-only, like `>>`
        self._reader = open(path, "rb")   # separate handle for random reads
        self.index: dict[str, int] = {}   # in-memory hash index
        self.rebuild_index()

    # ---- baseline: no index (this is your db_get from simplest_db.sh) ----

    def scan_get(self, key: str) -> str | None:
        """O(n): read the whole file, keep the last match."""
        result = None
        with open(self.path, "rb") as f:
            for line in f:
                k, v = decode(line)
                if k == key:
                    result = v
        return result

    # ---- the index: these three are yours ----

    def set(self, key: str, value: str) -> None:

        entry = encode(key, value)
        file_end = self._writer.tell()
        self.index[key] = file_end + 1
        self._writer.write(entry)
        self._writer.flush()
        # TODO (the crucial part): append the record AND keep the index correct.
        # 1. Find the byte offset where this record is about to start.
        #    (self._writer is in append mode, so self._writer.tell() is the end of the file.)
        # 2. Append encode(key, value) via self._writer.write(...), then self._writer.flush()
        #    so self._reader can see it.
        # 3. Point the index at the new record.
        #    Question to ask yourself: what happens to the old offset if the key already existed?

    def get(self, key: str) -> str | None:
        if key not in self.index:
            return
        byte_offset = self.index[key]
        self._reader.seek(byte_offset)
        _, value = decode(self._reader.readline())
        return value
        # TODO (the crucial part): one dict lookup + one seek, no scanning.
        # 1. Look up the offset in self.index. If the key isn't there, return None.
        # 2. self._reader.seek(offset), then self._reader.readline() reads exactly one record.
        # 3. decode(...) it and return the value.

    def rebuild_index(self) -> None:

        lines = self._reader.readlines()
        byte_offset = 0
        for line in lines:
            key, value = decode(line)
            self.index[key] = byte_offset
            byte_offset += len(line)
        # TODO (the crucial part): the index lives only in RAM, so after a restart it's gone.
        # Rebuild it by scanning the file once from the start.
        # - Open self.path in "rb" and iterate lines.
        # - Keep a running byte offset: each line starts where the previous one ended
        #   (offset += len(line), using bytes, not characters).
        # - For every line, set self.index[key] = offset_where_this_line_started.
        #   Later lines overwrite earlier ones, so the last write wins, same as `tail -n 1`.

    def file_size(self) -> int:
        return os.path.getsize(self.path)

    def close(self) -> None:
        self._writer.close()
        self._reader.close()
