@echo off
REM ============================================================
REM  Blog Writing Crew - Runner
REM  Run setup.bat first if you haven't already.
REM ============================================================

if not exist ".venv" (
    echo Virtual environment not found. Running setup first...
    call setup.bat
)

echo Starting Blog Writing Crew...
echo Output will be saved to: output\blog_post.md and output\social_posts.md
echo.

call .venv\Scripts\activate.bat
python run.py

echo.
echo Done! Check the output\ folder for your blog post and social media content.
pause
