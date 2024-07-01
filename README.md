# Spotify Track Popularity Application

This Python application allows users to fetch and sort an artist's tracks by popularity using the Spotify API. It provides a comprehensive view of an artist's discography, including tracks from albums and singles, sorted by their popularity scores.

## Features

- Fetch an artist's complete discography (albums and singles)
- Retrieve popularity scores for all tracks
- Sort tracks by popularity in descending order
- Display results in a formatted table

## Prerequisites

Before running this application, you need to have:

1. Python 3.x installed
2. A Spotify Developer account
3. A Spotify API Client ID and Client Secret

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/spotify-track-popularity.git
   cd spotify-track-popularity
   ```

2. Install the required packages:
   ```
   pip install requests tabulate
   ```

## Usage

1. Run the script:
   ```
   python spotify_track_popularity.py
   ```

2. When prompted, enter your Spotify API Client ID and Client Secret.

3. Enter the Spotify Artist ID for the artist you want to analyze. You can find an artist's ID by looking at their Spotify URL. For example, in the URL `https://open.spotify.com/artist/1vCWHaC5f2uS3yhpwWbIA6`, the artist ID is `1vCWHaC5f2uS3yhpwWbIA6`.

4. The application will fetch the data and display a table of the artist's tracks sorted by popularity.

## Output

The application will display a table with the following columns:

- Rank
- Track Name
- Popularity Score
- Spotify URL

## Note

This application respects Spotify API rate limits and uses pagination to fetch complete datasets. However, for artists with very large discographies, the process may take some time.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/VahidJbrl/SpotiRank/issues) if you want to contribute.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Spotify for providing the API
- The `requests` library for simplifying HTTP requests
- The `tabulate` library for formatting the output table
