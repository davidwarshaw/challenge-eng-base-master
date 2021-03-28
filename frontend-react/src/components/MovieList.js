import React from "react";

import { makeStyles } from "@material-ui/core/styles";
import Backdrop from "@material-ui/core/Backdrop";
import CircularProgress from "@material-ui/core/CircularProgress";
import Typography from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import Container from "@material-ui/core/Container";

import MovieCard from "./MovieCard";

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    padding: theme.spacing(2),
  },
  backdrop: {
    zIndex: theme.zIndex.drawer + 1,
    color: "#fff",
  },
}));

export default function MovieList(props) {
  const classes = useStyles();

  const { rows, chips, loading, handleClick, handleDelete } = props;
  // Waiting view
  if (loading) {
    return (
      <Backdrop className={classes.backdrop} open={loading}>
        <CircularProgress color="inherit" />
      </Backdrop>
    );
  }
  // No content view
  if (rows.length === 0) {
    return (
      <Container maxWidth="lg" className={classes.root}>
        <Typography variant="h5" component="h2">
          No Movies Found
        </Typography>
      </Container>
    );
  }
  // Content view
  return (
    <Grid container justify="center" className={classes.root} spacing={2}>
      {rows.map((movie, i) => (
        <Grid key={movie.id} xs={12} item>
          <MovieCard
            movie={movie}
            chips={chips[i]}
            handleClick={handleClick}
            handleDelete={handleDelete}
          />
        </Grid>
      ))}
    </Grid>
  );
}
