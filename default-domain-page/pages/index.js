import Head from "next/head";

const page = props => {
  return (
    <div>
      <Head>
        <title>{props.domain}</title>
        <link
          href="https://fonts.googleapis.com/css?family=IBM+Plex+Mono|IBM+Plex+Sans&display=swap"
          rel="stylesheet"
        />
      </Head>
      <center>
        <h1>{props.domain}</h1>
        <p>
          You can reach me on{" "}
          <a
            href={`mailto:ondrej@ondrejsika.com?subject=[parking] Domain ${props.domain}`}
          >
            ondrej@ondrejsika.com
          </a>
          .
        </p>
      </center>

      <style jsx global>{`
        h1 {
          font-family: "IBM Plex Mono", monospace;
        }
        a,
        p {
          font-family: "IBM Plex Sans", sans-serif;
        }
      `}</style>
    </div>
  );
};

page.getInitialProps = ({ req }) => {
  let host = req ? req.headers.host : window.location.hostname;
  return {
    domain: host
  };
};

export default page;
