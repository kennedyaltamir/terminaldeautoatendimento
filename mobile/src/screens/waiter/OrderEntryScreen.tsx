import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, FlatList, SafeAreaView, TouchableOpacity, TextInput, ActivityIndicator } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { useWaiterStore } from '../../store/waiter.store';
import { useSessionStore } from '../../store/session.store';
import { api } from '../../services/api';
import { colors } from '../../ui/tokens/colors';
import { spacing } from '../../ui/tokens/spacing';
import { typography } from '../../ui/tokens/typography';
import { Search, ChevronLeft, Plus, Minus, ShoppingCart } from 'lucide-react-native';
import { logger } from '../../services/logger.service';

const TAG = 'OrderEntryScreen';

export default function OrderEntryScreen() {
  const navigation = useNavigation<any>();
  const [menu, setMenu] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [activeCategory, setActiveCategory] = useState<number | null>(null);

  const slug = useSessionStore(state => state.slug);
  const { selectedTableNumber, cart, addToCart, updateQuantity, getCartTotal } = useWaiterStore();

  useEffect(() => {
    const fetchMenu = async () => {
      try {
        const response = await api.get(`/${slug}/menu`);
        setMenu(response.data);
        if (response.data.categories.length > 0) {
          setActiveCategory(response.data.categories[0].id);
        }
      } catch (e) {
        logger.error(TAG, 'Erro ao carregar menu', e);
      } finally {
        setLoading(false);
      }
    };
    fetchMenu();
  }, [slug]);

  const filteredProducts = menu?.categories
    .find((c: any) => c.id === activeCategory)
    ?.products.filter((p: any) => p.name.toLowerCase().includes(search.toLowerCase())) || [];

  const renderProduct = ({ item }: { item: any }) => {
    const cartItem = cart.find(i => i.productId === item.id);
    
    return (
      <View style={styles.productCard}>
        <View style={styles.productInfo}>
          <Text style={styles.productName}>{item.name}</Text>
          <Text style={styles.productPrice}>R$ {Number(item.price).toFixed(2)}</Text>
        </View>

        {cartItem ? (
          <View style={styles.counter}>
            <TouchableOpacity onPress={() => updateQuantity(item.id, -1)} style={styles.counterBtn}>
              <Minus size={16} color={colors.primary} />
            </TouchableOpacity>
            <Text style={styles.counterText}>{cartItem.quantity}</Text>
            <TouchableOpacity onPress={() => updateQuantity(item.id, 1)} style={styles.counterBtn}>
              <Plus size={16} color={colors.primary} />
            </TouchableOpacity>
          </View>
        ) : (
          <TouchableOpacity 
            onPress={() => addToCart({ id: item.id, name: item.name, price: Number(item.price) })}
            style={styles.addBtn}
          >
            <Plus size={20} color="#FFF" />
          </TouchableOpacity>
        )}
      </View>
    );
  };

  if (loading) return <View style={styles.center}><ActivityIndicator color={colors.primary} /></View>;

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backBtn}>
          <ChevronLeft color={colors.text.primary} />
        </TouchableOpacity>
        <View>
          <Text style={styles.headerTitle}>Mesa #{selectedTableNumber}</Text>
          <Text style={styles.headerSubtitle}>Lançamento de Itens</Text>
        </View>
      </View>

      <View style={styles.searchBar}>
        <Search size={18} color={colors.text.muted} style={styles.searchIcon} />
        <TextInput 
          placeholder="Buscar produto..." 
          placeholderTextColor={colors.text.muted}
          style={styles.searchInput}
          value={search}
          onChangeText={setSearch}
        />
      </View>

      <View style={styles.categories}>
        <FlatList 
          horizontal
          data={menu?.categories}
          keyExtractor={(item) => item.id.toString()}
          showsHorizontalScrollIndicator={false}
          renderItem={({ item }) => (
            <TouchableOpacity 
              onPress={() => setActiveCategory(item.id)}
              style={[styles.categoryTab, activeCategory === item.id && styles.categoryTabActive]}
            >
              <Text style={[styles.categoryText, activeCategory === item.id && styles.categoryTextActive]}>
                {item.name}
              </Text>
            </TouchableOpacity>
          )}
        />
      </View>

      <FlatList 
        data={filteredProducts}
        renderItem={renderProduct}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={styles.productList}
      />

      {cart.length > 0 && (
        <TouchableOpacity 
          style={styles.footerCart} 
          activeOpacity={0.9}
          onPress={() => navigation.navigate('OrderReview')}
        >
          <View style={styles.cartInfo}>
            <View style={styles.cartBadge}>
              <Text style={styles.cartBadgeText}>{cart.length}</Text>
            </View>
            <Text style={styles.cartTotal}>R$ {getCartTotal().toFixed(2)}</Text>
          </View>
          <View style={styles.cartAction}>
            <Text style={styles.cartActionText}>Revisar Pedido</Text>
            <ShoppingCart size={18} color="#FFF" />
          </View>
        </TouchableOpacity>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: colors.background },
  header: { padding: spacing.lg, flexDirection: 'row', alignItems: 'center', gap: spacing.md },
  backBtn: { padding: spacing.sm, backgroundColor: colors.surface, borderRadius: 12 },
  headerTitle: { fontSize: typography.size.md, fontWeight: 'bold', color: colors.text.primary },
  headerSubtitle: { fontSize: 10, color: colors.text.muted, textTransform: 'uppercase' },
  searchBar: { margin: spacing.lg, flexDirection: 'row', alignItems: 'center', backgroundColor: colors.surface, borderRadius: 12, paddingHorizontal: spacing.md },
  searchIcon: { marginRight: spacing.sm },
  searchInput: { flex: 1, height: 48, color: colors.text.primary },
  categories: { paddingLeft: spacing.lg, marginBottom: spacing.md },
  categoryTab: { paddingHorizontal: spacing.lg, paddingVertical: spacing.sm, borderRadius: 20, marginRight: spacing.sm, backgroundColor: colors.surface },
  categoryTabActive: { backgroundColor: colors.primary },
  categoryText: { fontSize: 12, fontWeight: 'bold', color: colors.text.secondary },
  categoryTextActive: { color: '#FFF' },
  productList: { padding: spacing.lg },
  productCard: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', backgroundColor: colors.surface, padding: spacing.lg, borderRadius: 16, marginBottom: spacing.md },
  productInfo: { flex: 1 },
  productName: { fontSize: 16, fontWeight: 'bold', color: colors.text.primary, marginBottom: 4 },
  productPrice: { fontSize: 14, color: colors.primary, fontWeight: 'bold' },
  addBtn: { width: 40, height: 40, borderRadius: 20, backgroundColor: colors.primary, alignItems: 'center', justifyContent: 'center' },
  counter: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, backgroundColor: colors.background, padding: 4, borderRadius: 20 },
  counterBtn: { width: 32, height: 32, borderRadius: 16, backgroundColor: colors.surface, alignItems: 'center', justifyContent: 'center' },
  counterText: { color: colors.text.primary, fontWeight: 'bold', minWidth: 20, textAlign: 'center' },
  footerCart: { position: 'absolute', bottom: spacing.xl, left: spacing.lg, right: spacing.lg, height: 64, backgroundColor: colors.primary, borderRadius: 20, flexDirection: 'row', alignItems: 'center', paddingHorizontal: spacing.xl, shadowColor: colors.primary, shadowOffset: { width: 0, height: 10 }, shadowOpacity: 0.3, shadowRadius: 20, elevation: 10 },
  cartInfo: { flex: 1, flexDirection: 'row', alignItems: 'center', gap: spacing.md },
  cartBadge: { backgroundColor: '#FFF', width: 24, height: 24, borderRadius: 12, alignItems: 'center', justifyContent: 'center' },
  cartBadgeText: { color: colors.primary, fontSize: 12, fontWeight: 'bold' },
  cartTotal: { color: '#FFF', fontSize: 18, fontWeight: 'black' },
  cartAction: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  cartActionText: { color: '#FFF', fontWeight: 'bold' }
});
