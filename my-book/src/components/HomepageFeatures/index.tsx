import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';
import image1Image from '@site/static/img/image1.png';
import image2ModuleImage from '@site/docs/assets/image2.png';
import image3ModuleImage from '@site/docs/assets/image3.png';
import image4ModuleImage from '@site/docs/assets/image4.png';

type FeatureItem = {
  title: string;
  Svg?: React.ComponentType<React.ComponentProps<'svg'>>;
  imgSrc?: string;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Module 1:',
    imgSrc: image1Image,
    description: (
      <>
      The Robotic Nervous System (ROS 2)
      </>
    ),
  },
  {
    title: 'Module 2:',
    imgSrc: image2ModuleImage,
    description: (
      <>
      The Digital Twin (Gazebo & Unity)
      </>
    ),
  },
  {
    title: 'Module 3:',
    imgSrc: image3ModuleImage,
    description: (
      <>
       The AI-Robot Brain (NVIDIA Isaac)
      </>
    ),
      },
    {
      title: 'Module 4:',
      imgSrc: image4ModuleImage,
      description: (
        <>
        Vision-Language-Action (VLA)
        </>
      ),
    },
  ];
function Feature({title, Svg, imgSrc, description, link}: FeatureItem) {
  return (
    <div className={clsx('col col--3')}>
      <div className="text--center">
        {link ? (
          <a href={link}>
            {imgSrc ? (
              <img src={imgSrc} className={styles.featureSvg} alt={title} />
            ) : (
              <Svg className={styles.featureSvg} role="img" />
            )}
          </a>
        ) : (
          imgSrc ? (
            <img src={imgSrc} className={styles.featureSvg} alt={title} />
          ) : (
            <Svg className={styles.featureSvg} role="img" />
          )
        )}
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
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
