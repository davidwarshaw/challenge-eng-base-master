import React, { useState, useEffect } from "react";

import SearchBar from "./SearchBar";
import Selected from "./Selected";
import MovieList from "./MovieList";
import Pagination from "./Pagination";
import ErrorAlert from "./ErrorAlert";

const chipsFromGenresAndTags = (genres, tags, selectedGenres, selectedTags) => {
  const genreChips = genres.map((genre) => ({
    label: genre,
    type: "genre",
    color: "primary",
    variant: selectedGenres.includes(genre) ? "default" : "outlined",
  }));
  const tagChips = tags.map((tag) => ({
    label: tag,
    type: "tag",
    color: "secondary",
    variant: selectedTags.includes(tag) ? "default" : "outlined",
  }));
  return [...genreChips, ...tagChips];
};

const chipsFromMovies = (movies, selectedGenres, selectedTags) =>
  movies.map((movie) =>
    chipsFromGenresAndTags(
      movie.genres,
      movie.tags,
      selectedGenres,
      selectedTags
    )
  );

export default function App() {
  // Request state
  const [q, setQ] = useState("");
  const [selectedGenres, setSelectedGenres] = useState([]);
  const [selectedTags, setSelectedTags] = useState([]);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  // Response state
  const [rowCount, setRowCount] = useState(0);
  const [movieRows, setMovieRows] = useState([]);
  const [movieChips, setMovieChips] = useState([]);
  // Util state
  const [loadingMovies, setLoadingMovies] = useState(false);
  const [error, setError] = useState("");

  const fetchMovies = (resetPage) => {
    // Join genres and tags for query param-ification
    const genresJoined = selectedGenres.join(",");
    const tagsJoined = selectedTags.join(",");
    // Put up the waiting indicator
    setLoadingMovies(true);
    const fetchPage = resetPage ? 1 : page;
    fetch(
      `/movies?q=${q}&genres=${genresJoined}&tags=${tagsJoined}&page=${fetchPage}&page_size=${pageSize}`
    )
      .then((res) => res.json())
      .then((body) => {
        // Merge the genre and tags together to be put into the chips
        const chips = chipsFromMovies(body.data, selectedGenres, selectedTags);
        // Set the top level state
        setPage(body.pagination.page);
        setPageSize(body.pagination.page_size);
        setRowCount(body.pagination.row_count);
        setMovieRows(body.data);
        setMovieChips(chips);
        setLoadingMovies(false);
      })
      .catch((err) => {
        // Reset the state to initial
        setPage(1);
        setPageSize(20);
        setRowCount(0);
        setMovieRows([]);
        setMovieChips([]);
        setLoadingMovies(false);
        // Put up the error snackbar
        setError(err);
      });
  };

  useEffect(() => fetchMovies(true), [q, selectedGenres, selectedTags]);
  useEffect(() => fetchMovies(false), [page, pageSize]);

  // Handlers to pass down to child components
  const handleQChange = (event) => setQ(event.target.value);
  const handlePageChange = (_, value) => setPage(value);
  const handleErrorClose = () => setError("");
  const handleChipClickClosure = (type, selectedLabel) => (e) => {
    if (type === "genre") {
      const updated = [...selectedGenres, selectedLabel];
      setSelectedGenres(updated);
    } else {
      const updated = [...selectedTags, selectedLabel];
      setSelectedTags(updated);
    }
  };
  const handleChipDeleteClosure = (type, deletedLabel) => (e) => {
    if (type === "genre") {
      const updated = selectedGenres.filter((label) => label !== deletedLabel);
      setSelectedGenres(updated);
    } else {
      const updated = selectedTags.filter((label) => label !== deletedLabel);
      setSelectedTags(updated);
    }
  };

  // Create chips from the selected genres and tags
  const selectedChips = chipsFromGenresAndTags(
    selectedGenres,
    selectedTags,
    selectedGenres,
    selectedTags
  );

  return (
    <div>
      <SearchBar handleQChange={handleQChange} />
      <ErrorAlert error={error} handleErrorClose={handleErrorClose} />
      <Selected chips={selectedChips} handleDelete={handleChipDeleteClosure} />
      <MovieList
        rows={movieRows}
        chips={movieChips}
        loading={loadingMovies}
        handleClick={handleChipClickClosure}
        handleDelete={handleChipDeleteClosure}
      />
      <Pagination
        page={page}
        pageSize={pageSize}
        rowCount={rowCount}
        handlePageChange={handlePageChange}
      />
    </div>
  );
}
