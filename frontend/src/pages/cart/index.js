import { PurchaseList, Title, Container, Main, Button } from '../../components'
import styles from './styles.module.css'
import { useRecipes } from '../../utils/index.js'
import { useEffect, useState } from 'react'
import api from '../../api'
import MetaTags from 'react-meta-tags'

const Cart = ({ updateOrders, orders }) => {
  const {
    recipes,
    setRecipes,
    handleAddToCart
  } = useRecipes()
  
  const getRecipes = () => {
    api
      .getRecipes({
        page: 1,
        limit: 999,
        is_in_shopping_cart: Number(true)
      })
      .then(res => {
        const { results } = res
        setRecipes(results)
      })
  }

  useEffect(_ => {
    getRecipes()
  }, [])

  const downloadDocument = () => {
    api.downloadFile()
  }

  return <Main>
    <Container className={styles.container}>
      <MetaTags>
        <title>Shopping Cart</title>
        <meta name="description" content="Foodgram - Shopping Cart" />
        <meta property="og:title" content="Shopping Cart" />
      </MetaTags>
      <div className={styles.cart}>
        <Title title='Shopping Cart' />
        <PurchaseList
          orders={recipes}
          handleRemoveFromCart={handleAddToCart}
          updateOrders={updateOrders}
        />
        {orders > 0 && <Button
          modifier='style_dark-blue'
          clickHandler={downloadDocument}
        >Скачать список</Button>}
      </div>
    </Container>
  </Main>
}

export default Cart

