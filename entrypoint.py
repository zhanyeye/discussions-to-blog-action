#!/usr/bin/env python3  

import argparse  
from discussions_to_blog import run  

def main():  
    parser = argparse.ArgumentParser(description="Convert GitHub Discussions to Blog Posts")  
    parser.add_argument('--categories', required=True, help="Comma-separated list of categories (e.g., Announcements, General)")  
    parser.add_argument('--output_dir', default="content/posts", help="Directory to output markdown files (default: content/posts)")  
    args = parser.parse_args()  

    run(output_dir=args.output_dir, categories=[cat.strip().lower() for cat in args.categories.split(",")])  

if __name__ == "__main__":  
    main()  