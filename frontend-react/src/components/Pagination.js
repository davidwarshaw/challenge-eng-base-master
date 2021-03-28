import React from "react";

import { makeStyles } from "@material-ui/core/styles";
import Typography from "@material-ui/core/Typography";
import Pagination from "@material-ui/lab/Pagination";
import Container from "@material-ui/core/Container";

const useStyles = makeStyles((theme) => ({
  root: {
    "& > * + *": {
      marginTop: theme.spacing(2),
    },
  },
}));

export default function PaginationControlled(props) {
  const classes = useStyles();

  const { page, pageSize, rowCount, handlePageChange, loading } = props;
  const count = Math.ceil(rowCount / pageSize);
  return (
    <Container maxWidth="lg">
      {/* <Typography>Page: {page}</Typography> */}
      <Pagination
        count={count}
        page={page}
        onChange={handlePageChange}
        showFirstButton
        showLastButton
      />
    </Container>
  );
}
