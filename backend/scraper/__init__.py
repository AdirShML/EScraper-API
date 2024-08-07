from main import main
import sys


if __name__ == '__main__':
    # Extract command-line arguments
    if len(sys.argv) < 2:
        print('Usage: python -m package_name url search_text endpoint')
        sys.exit(1)

    search_text = sys.argv[1]
    endpoint = sys.argv[2]

    # Run the scraper asynchronously
    main(search_text, endpoint)