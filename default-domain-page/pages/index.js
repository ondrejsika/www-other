import Head from "next/head";

const page = props => {
  return (
    <div>
      <Head>
        <title>{props.domain}</title>
      </Head>
      <h1>{props.domain}</h1>
      <p>
        You can reach me on{" "}
        <a href="mailto:ondrej@ondrejsika.com">ondrej@ondrejsika.com</a>.
      </p>
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
