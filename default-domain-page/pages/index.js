import Head from "next/head";

const page = props => {
  let domain = props.domain;

  let title = `${domain} - Ondrej Sika's Domain`;

  return (
    <div>
      <Head>{title}</Head>
      <h1>{title}</h1>
      <p>You can reach me on <a href="mailto:ondrej@ondrejsika.com">ondrej@ondrejsika.com</a>.</p>
    </div>
  );
};

page.getInitialProps = ({ req }) => {
  let host = req ? req.headers.host : window.location.hostname;
  return {
    domain: host,
  };
};

export default page;
