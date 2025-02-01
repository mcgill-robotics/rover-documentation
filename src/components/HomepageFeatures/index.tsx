import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  Svg?: React.ComponentType<React.ComponentProps<'svg'>>;
  Png?: string; // Use string type for PNG since it's imported as a path
  description: JSX.Element;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Halley',
    Svg: require('@site/static/img/roverstickergalileo.svg').default,
    description: (
      <>
        2025
      </>
    ),
  },
  {
    title: 'Galileo',
    Png: require('@site/static/img/rover+sticker+galileo.png').default,
    description: (
      <>
        2023-2024
      </>
    ),
  },
  {
    title: 'Fourier',
    Png: require('@site/static/img/fourier+robot+cropped.png').default,
    description: (
      <>
        2021-2023
      </>
    ),
  }
];


// Now thats my kind of version control :p
// function Feature({title, Svg, description}: FeatureItem) {
//   return (
//     <div className={clsx('col col--4')}>
//       <div className="text--center">
//         <Svg className={styles.featureSvg} role="img" />
//       </div>
//       <div className="text--center padding-horiz--md">
//         <Heading as="h3">{title}</Heading>
//         <p>{description}</p>
//       </div>
//     </div>
//   );
// }

function Feature({ title, Svg, Png, description }: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        {Png ? (
          <img src={Png} alt={title} className={styles.featureImg} /> // Render PNG if available
        ) : Svg ? (
          <Svg className={styles.featureSvg} role="img" />
        ) : null}
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): JSX.Element {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
