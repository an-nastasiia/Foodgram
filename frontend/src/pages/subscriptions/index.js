import { Title, Pagination, Container, Main, SubscriptionList  } from '../../components'
import { useSubscriptions } from '../../utils'
import api from '../../api'
import { useEffect } from 'react'
import MetaTags from 'react-meta-tags'

const SubscriptionsPage = () => {
  const {
    subscriptions,
    setSubscriptions,
    subscriptionsCount,
    setSubscriptionsCount,
    removeSubscription,
    subscriptionsPage,
    setSubscriptionsPage
  } = useSubscriptions()

  const getSubscriptions = ({ page }) => {
    api
      .getSubscriptions({ page })
      .then(res => {
        setSubscriptions(res.results)
        setSubscriptionsCount(res.count)
      })
  }

  useEffect(_ => {
    getSubscriptions({ page: subscriptionsPage })
  }, [subscriptionsPage])


  return <Main>
    <Container>
      <MetaTags>
        <title>Subscriptions</title>
        <meta name="description" content="Foodgram - Subscriptions" />
        <meta property="og:title" content="Subscriptions" />
      </MetaTags>
      <Title
        title='Subscriptions'
      />
      <SubscriptionList
        subscriptions={subscriptions}
        removeSubscription={removeSubscription}
      />
      <Pagination
        count={subscriptionsCount}
        limit={6}
        onPageChange={page => {
          setSubscriptionsPage(page)
        }}
      />
    </Container>
  </Main>
}

export default SubscriptionsPage