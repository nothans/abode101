# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "piexif==1.1.3",
#     "pillow==13.0.0",
#     "pymupdf==2.1",
# ]
# ///
"""Show or set the embedded metadata of a knowledge-base artifact: JPEG, PNG, PDF, MP4/M4A/MOV, MP3.

usage:
  uv run artifact_meta.py show <file>
  uv run artifact_meta.py set <file> --title "..." [--description "..."] [--subject "..."] [--keywords "a;b;c"]
                                     [--author "..."] [--comment "..."] [--date YYYY-MM-DD] [--out <file>]

One vocabulary, mapped per format:
  title        JPEG XPTitle            PNG tEXt Title         PDF /Title      MP4 title       MP3 TIT2 (title)
  description  JPEG ImageDescription   PNG tEXt Description   PDF /Subject    MP4 description MP3 comment
               + UserComment
  subject      JPEG XPSubject          PNG tEXt Subject       (in /Subject)   MP4 show/album  MP3 album
  keywords     JPEG XPKeywords         PNG tEXt Keywords      PDF /Keywords   MP4 keywords    MP3 (in comment)
  author       JPEG Artist             PNG tEXt Author        PDF /Author     MP4 artist      MP3 TPE1 (artist)
  comment      JPEG XPComment          PNG tEXt Comment       (in /Keywords)  MP4 comment     MP3 comment
  date         JPEG DateTimeOriginal (only if the file has none)  PNG Creation Time  PDF /CreationDate (if none)

Pixels, pages, and streams are never re-encoded: JPEG via piexif.insert, PNG via a chunk rewrite,
PDF via an incremental info update, audio/video via ffmpeg -c copy. uv installs piexif, Pillow, and PyMuPDF
from the header above; MP4/MP3 need ffmpeg on PATH or FFMPEG=<path>.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

KEYS = ['title', 'description', 'subject', 'keywords', 'author', 'comment', 'date']


def ffmpeg():
    f = os.environ.get('FFMPEG') or shutil.which('ffmpeg')
    if not f:
        sys.exit('ffmpeg not found: put it on the PATH or set FFMPEG=<path to ffmpeg>')
    return f


# ---------- JPEG ----------
def ucs2(s):
    return s.encode('utf-16le') + b'\x00\x00'


def unucs2(v):
    b = bytes(v) if not isinstance(v, bytes) else v
    return b.decode('utf-16le', 'replace').rstrip('\x00')


def jpeg_show(path):
    import piexif
    ex = piexif.load(path)
    I, E = piexif.ImageIFD, piexif.ExifIFD
    z = ex['0th']
    out = {
        'title': unucs2(z[I.XPTitle]) if I.XPTitle in z else None,
        'description': z.get(I.ImageDescription, b'').decode('utf-8', 'replace') or None,
        'subject': unucs2(z[I.XPSubject]) if I.XPSubject in z else None,
        'keywords': unucs2(z[I.XPKeywords]) if I.XPKeywords in z else None,
        'author': z.get(I.Artist, b'').decode('utf-8', 'replace') or None,
        'comment': unucs2(z[I.XPComment]) if I.XPComment in z else None,
        'date': ex['Exif'].get(E.DateTimeOriginal, b'').decode('ascii', 'replace') or None,
    }
    return out


def jpeg_set(path, out, m):
    import piexif
    ex = piexif.load(path)
    I, E = piexif.ImageIFD, piexif.ExifIFD
    z = ex['0th']
    if m.get('title'): z[I.XPTitle] = ucs2(m['title'])
    if m.get('description'):
        z[I.ImageDescription] = m['description'].encode('utf-8')
        ex['Exif'][E.UserComment] = b'UNICODE\x00' + m['description'].encode('utf-16be')
    if m.get('subject'): z[I.XPSubject] = ucs2(m['subject'])
    if m.get('keywords'): z[I.XPKeywords] = ucs2(m['keywords'])
    if m.get('author'): z[I.Artist] = m['author'].encode('utf-8')
    if m.get('comment'): z[I.XPComment] = ucs2(m['comment'])
    if m.get('date') and E.DateTimeOriginal not in ex['Exif']:
        ex['Exif'][E.DateTimeOriginal] = (m['date'].replace('-', ':') + ' 00:00:00').encode('ascii')
    if out != path:
        shutil.copy(path, out)
    piexif.insert(piexif.dump(ex), out)


# ---------- PNG ----------
PNG_KEYS = {'title': 'Title', 'description': 'Description', 'subject': 'Subject', 'keywords': 'Keywords',
            'author': 'Author', 'comment': 'Comment', 'date': 'Creation Time'}


def png_show(path):
    from PIL import Image
    im = Image.open(path)
    t = getattr(im, 'text', {}) or {}
    return {k: t.get(v) for k, v in PNG_KEYS.items()}


def png_set(path, out, m):
    from PIL import Image, PngImagePlugin
    im = Image.open(path)
    info = PngImagePlugin.PngInfo()
    existing = getattr(im, 'text', {}) or {}
    merged = dict(existing)
    for k, v in PNG_KEYS.items():
        if m.get(k):
            merged[v] = m[k]
    for k, v in merged.items():
        info.add_itxt(k, v) if any(ord(c) > 127 for c in v) else info.add_text(k, v)
    # a lossless re-save of the same pixels; palette/mode preserved
    im.save(out, format='PNG', pnginfo=info, optimize=False)


# ---------- PDF ----------
def pdf_show(path):
    import pymupdf
    d = pymupdf.open(path)
    md = d.metadata
    return {'title': md.get('title') or None, 'description': md.get('subject') or None, 'subject': None,
            'keywords': md.get('keywords') or None, 'author': md.get('author') or None, 'comment': None,
            'date': md.get('creationDate') or None}


def pdf_set(path, out, m):
    import pymupdf
    d = pymupdf.open(path)
    md = d.metadata
    if m.get('title'): md['title'] = m['title']
    subj = '. '.join(x for x in [m.get('subject'), m.get('description')] if x)
    if subj: md['subject'] = subj
    kw = '; '.join(x for x in [m.get('keywords'), m.get('comment')] if x)
    if kw: md['keywords'] = kw
    if m.get('author'): md['author'] = m['author']
    if m.get('date') and not md.get('creationDate'):
        md['creationDate'] = 'D:' + m['date'].replace('-', '') + '000000'
    d.set_metadata(md)
    if out == path:
        d.save(path, incremental=True, encryption=pymupdf.PDF_ENCRYPT_KEEP)
    else:
        d.save(out)


# ---------- MP4 / MP3 via ffmpeg ----------
AV_MAP = {
    'mp4': {'title': 'title', 'description': 'description', 'subject': 'show', 'keywords': 'keywords', 'author': 'artist', 'comment': 'comment', 'date': 'date'},
    'mp3': {'title': 'title', 'description': 'comment', 'subject': 'album', 'keywords': 'comment', 'author': 'artist', 'comment': 'comment', 'date': 'date'},
}


def av_show(path):
    r = subprocess.run([ffmpeg(), '-hide_banner', '-i', path], capture_output=True, text=True)
    tags = {}
    for line in r.stderr.splitlines():
        s = line.strip()
        if ':' in s and s.split(':')[0].strip().islower() and not s.startswith('Stream') and not s.startswith('Duration'):
            k, _, v = s.partition(':')
            tags.setdefault(k.strip(), v.strip())
    return {k: tags.get(v) for k, v in AV_MAP['mp4'].items()} | {'_all': tags}


def av_set(path, out, m, kind):
    ext = os.path.splitext(path)[1]
    tmp = out if out != path else os.path.join(os.path.dirname(path) or '.', '.' + os.path.basename(path) + '.tmp' + ext)
    cmd = [ffmpeg(), '-hide_banner', '-loglevel', 'error', '-y', '-i', path, '-map', '0', '-c', 'copy']
    if kind == 'mp4':
        cmd += ['-movflags', '+faststart']
    else:
        cmd += ['-id3v2_version', '3']
    for k, tag in AV_MAP[kind].items():
        if m.get(k):
            val = m[k] if not (kind == 'mp3' and tag == 'comment' and k != 'comment') else None
            if val:
                cmd += ['-metadata', f'{tag}={val}']
    if kind == 'mp3':
        parts = [x for x in [m.get('description'), m.get('keywords'), m.get('comment')] if x]
        if parts:
            cmd += ['-metadata', 'comment=' + ' | '.join(parts)]
    cmd += [tmp]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit('ffmpeg failed: ' + r.stderr[-500:])
    if tmp != out:
        os.replace(tmp, out)


def kind_of(path):
    e = os.path.splitext(path)[1].lower()
    return {'.jpg': 'jpeg', '.jpeg': 'jpeg', '.png': 'png', '.pdf': 'pdf', '.mp4': 'mp4', '.m4v': 'mp4', '.m4a': 'mp4', '.mov': 'mp4', '.mp3': 'mp3'}.get(e)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('action', choices=['show', 'set'])
    ap.add_argument('file')
    for k in KEYS:
        ap.add_argument('--' + k)
    ap.add_argument('--out', help='write to this file instead of in place')
    a = ap.parse_args()
    kind = kind_of(a.file)
    if not kind:
        sys.exit('unsupported file type: ' + a.file)
    if a.action == 'show':
        fn = {'jpeg': jpeg_show, 'png': png_show, 'pdf': pdf_show, 'mp4': av_show, 'mp3': av_show}[kind]
        for k, v in fn(a.file).items():
            if k != '_all':
                print(f'{k:12} {v if v is not None else "-"}')
        return
    m = {k: getattr(a, k) for k in KEYS if getattr(a, k)}
    if not m:
        sys.exit('nothing to set')
    out = a.out or a.file
    if kind == 'jpeg': jpeg_set(a.file, out, m)
    elif kind == 'png': png_set(a.file, out, m)
    elif kind == 'pdf': pdf_set(a.file, out, m)
    else: av_set(a.file, out, m, kind)
    print('wrote', out)


if __name__ == '__main__':
    main()
